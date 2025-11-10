"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Trash2, Volume2 } from "lucide-react";
import axios from "axios";

const API_URL =
  typeof window !== "undefined"
    ? `http://${window.location.hostname}:8000`
    : "http://localhost:8000";

interface HistoryItem {
  id: number;
  task_id: string;
  text: string;
  text_preview: string;
  confidence: number;
  word_count: number;
  created_at: string;
}

export default function HistoryPage() {
  const router = useRouter();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speakingId, setSpeakingId] = useState<number | null>(null);

  // 기록 불러오기
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`${API_URL}/api/history?limit=50`);
      if (response.data.success) {
        setHistory(response.data.data);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "기록을 불러올 수 없습니다");
    } finally {
      setIsLoading(false);
    }
  };

  // 기록 삭제
  const handleDelete = async (id: number) => {
    if (!confirm("이 기록을 삭제하시겠습니까?")) return;

    try {
      await axios.delete(`${API_URL}/api/history/${id}`);
      // 삭제 후 목록 새로고침
      setHistory(history.filter((item) => item.id !== id));
    } catch (err) {
      alert("삭제에 실패했습니다");
    }
  };

  // 음성 읽기
  const speak = (id: number, text: string) => {
    if ("speechSynthesis" in window) {
      if (isSpeaking && speakingId === id) {
        // 같은 항목 클릭 시 중지
        speechSynthesis.cancel();
        setIsSpeaking(false);
        setSpeakingId(null);
      } else {
        // 다른 항목 클릭 시 새로 읽기
        speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "ko-KR";
        utterance.rate = 0.8;
        utterance.onend = () => {
          setIsSpeaking(false);
          setSpeakingId(null);
        };
        utterance.onerror = () => {
          setIsSpeaking(false);
          setSpeakingId(null);
        };
        speechSynthesis.speak(utterance);
        setIsSpeaking(true);
        setSpeakingId(id);
      }
    } else {
      alert("음성 기능을 지원하지 않는 브라우저입니다");
    }
  };

  // 날짜 포맷
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) {
      return "오늘";
    } else if (days === 1) {
      return "어제";
    } else if (days < 7) {
      return `${days}일 전`;
    } else {
      return date.toLocaleDateString("ko-KR");
    }
  };

  return (
    <div className="min-h-screen p-2 sm:p-4">
      <div className="max-w-md mx-auto pt-2 sm:pt-4">
        {/* 메인 카드 */}
        <div className="card">
          {/* 헤더 */}
          <div className="mb-8 pb-6 border-b-2 border-amber-300">
            <div className="flex items-center mb-4">
              <button
                onClick={() => router.push("/")}
                className="w-12 h-12 rounded-full bg-amber-100 hover:bg-amber-200 flex items-center justify-center transition-all"
              >
                <ArrowLeft className="w-7 h-7 text-amber-800" />
              </button>
              <h1 className="flex-1 text-4xl font-bold text-amber-900 text-center">
                지난 기록
              </h1>
              <div className="w-12" /> {/* 균형 맞추기 */}
            </div>
            <p className="text-lg text-amber-700 font-medium text-center">
              이전에 읽은 내용들을 다시 볼 수 있어요
            </p>
          </div>

          {/* 로딩 */}
          {isLoading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-4 border-yellow-500 mb-4"></div>
              <p className="text-amber-700 mt-4">기록 불러오는 중...</p>
            </div>
          )}

          {/* 에러 */}
          {error && (
            <div className="text-center py-12">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {/* 기록 목록 */}
          {!isLoading && !error && (
            <>
              {history.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-amber-700 text-lg mb-6">
                    아직 촬영 기록이 없습니다
                  </p>
                  <button
                    onClick={() => router.push("/")}
                    className="bg-yellow-400 hover:bg-yellow-500 text-amber-900 font-bold py-4 px-8 rounded-3xl transition-all"
                  >
                    첫 촬영 시작하기
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {history.map((item) => (
                    <div
                      key={item.id}
                      className="bg-yellow-100 rounded-3xl p-5"
                    >
                      {/* 날짜 */}
                      <div className="text-sm text-amber-600 font-medium mb-3">
                        📅 {formatDate(item.created_at)}
                      </div>

                      {/* 텍스트 미리보기 */}
                      <p className="text-amber-900 mb-4 ocr-text line-clamp-3 text-base">
                        {item.text_preview}
                      </p>

                      {/* 정보 */}
                      <div className="flex gap-4 text-sm text-amber-700 mb-4">
                        <span className="font-medium">
                          글자 {item.word_count}개
                        </span>
                        <span className="font-medium">
                          정확도 {item.confidence}%
                        </span>
                      </div>

                      {/* 버튼들 */}
                      <div className="flex gap-2">
                        <button
                          onClick={() => speak(item.id, item.text)}
                          className={`flex-1 py-3 rounded-3xl font-bold transition-all ${
                            isSpeaking && speakingId === item.id
                              ? "bg-red-500 hover:bg-red-600 text-white"
                              : "bg-yellow-200 hover:bg-yellow-300 text-amber-900"
                          }`}
                        >
                          <Volume2 className="w-5 h-5 inline mr-2" />
                          {isSpeaking && speakingId === item.id
                            ? "멈추기"
                            : "듣기"}
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="px-5 py-3 rounded-3xl bg-red-100 text-red-600 hover:bg-red-200 transition-all font-bold"
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
