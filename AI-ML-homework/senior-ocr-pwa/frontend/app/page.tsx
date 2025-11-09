"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Camera, Upload, History } from "lucide-react";
import axios from "axios";

// 자동으로 현재 호스트 사용 (모바일/PC 모두 동작)
const API_URL =
  typeof window !== "undefined"
    ? `http://${window.location.hostname}:8000`
    : "http://localhost:8000";

export default function Home() {
  const router = useRouter();
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = async (file: File) => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(`${API_URL}/api/ocr`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.data.success) {
        setResult(response.data.data);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "처리 중 오류가 발생했습니다");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleImageUpload(file);
    }
  };

  const speak = (text: string) => {
    if ("speechSynthesis" in window) {
      if (isSpeaking) {
        // 음성 중지
        speechSynthesis.cancel();
        setIsSpeaking(false);
      } else {
        // 음성 시작
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "ko-KR";
        utterance.rate = 0.8; // 천천히
        utterance.pitch = 1;
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = () => setIsSpeaking(false);
        speechSynthesis.speak(utterance);
        setIsSpeaking(true);
      }
    } else {
      alert("음성 기능을 지원하지 않는 브라우저입니다");
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert("복사되었습니다!");
  };

  // 결과 화면 (OCR 완료 후)
  if (result) {
    return (
      <div className="min-h-screen p-4 sm:p-6">
        <div className="max-w-md mx-auto pt-6">
          {/* 결과 카드: OCR 텍스트 표시 영역 */}
          <div className="card">
            {/* 헤더 */}
            <div className="mb-6 pb-6 border-b-2 border-yellow-200">
              <h1 className="text-3xl font-bold text-amber-800 text-center">
                읽어드림
              </h1>
            </div>

            <p className="text-lg text-amber-800 font-semibold mb-6 text-center leading-relaxed">
              ✅ 글씨를 찾았어요!
              <br />
              아래 내용을 확인해주세요
            </p>

            {/* 결과 텍스트 박스: 스크롤 가능, 최대 높이 40vh */}
            <div className="bg-yellow-100 rounded-3xl p-6 mb-6 max-h-[40vh] overflow-auto">
              <p className="text-xl leading-relaxed ocr-text text-amber-900">
                {result.text || "글씨를 찾을 수 없어요"}
              </p>
            </div>

            {/* 상세 정보: 단어 수, 정확도 표시 */}
            <div className="bg-yellow-100 rounded-3xl p-5 mb-6 space-y-3">
              <div className="flex justify-between py-2">
                <span className="text-amber-700 text-base font-medium">
                  글자 개수
                </span>
                <span className="font-bold text-amber-900 text-lg">
                  {result.word_count}개
                </span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-amber-700 text-base font-medium">
                  정확도
                </span>
                <span className="font-bold text-amber-900 text-lg">
                  {result.confidence}%
                </span>
              </div>
            </div>

            {/* 메인 버튼: TTS (음성 읽기) 토글 */}
            <button
              onClick={() => speak(result.text)}
              className={`w-full py-5 rounded-3xl font-bold text-lg mb-4 transition-all ${
                isSpeaking
                  ? "bg-red-500 hover:bg-red-600 text-white"
                  : "bg-yellow-300 hover:bg-yellow-400 text-amber-900"
              }`}
            >
              {isSpeaking ? "⏹️ 소리 멈추기" : "🔊 소리로 읽어주기"}
            </button>
            <p className="text-sm text-amber-700 text-center mb-6">
              {isSpeaking
                ? "소리로 읽고 있어요"
                : "버튼을 누르면 소리로 읽어드려요"}
            </p>

            {/* 하단 버튼들: 다시 촬영, 복사 */}
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                  setResult(null);
                  setError(null);
                  setIsSpeaking(false);
                  speechSynthesis.cancel();
                }}
                className="bg-yellow-100 hover:bg-yellow-200 rounded-3xl p-5 transition-all"
              >
                <div className="text-center">
                  <p className="text-lg font-bold text-amber-900">
                    🔄 다시 찍기
                  </p>
                  <p className="text-xs text-amber-700 mt-1">
                    처음으로 돌아가요
                  </p>
                </div>
              </button>

              <button
                onClick={() => copyToClipboard(result.text)}
                className="bg-yellow-100 hover:bg-yellow-200 rounded-3xl p-5 transition-all"
              >
                <div className="text-center">
                  <p className="text-lg font-bold text-amber-900">
                    📋 복사하기
                  </p>
                  <p className="text-xs text-amber-700 mt-1">
                    붙여넣을 수 있어요
                  </p>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // 메인 화면 (OCR 촬영 대기)
  return (
    <div className="min-h-screen p-4 sm:p-6">
      <div className="max-w-md mx-auto pt-6">
        {/* 통합 메인 카드: 헤더 + 촬영 UI */}
        <div className="card">
          {/* 헤더 */}
          <div className="mb-6 pb-6 border-b-2 border-yellow-200">
            <h1 className="text-3xl font-bold text-amber-800 text-center leading-tight">
              읽어드림
              <p className="text-lg text-amber-800 font-semibold mb-6 text-center">
                사진을 찍으면 글씨를 크게 보여드려요!
              </p>
            </h1>
          </div>

          {isProcessing ? (
            /* 로딩 스피너 */
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-yellow-500 mb-6"></div>
              <p className="text-xl text-amber-800 font-bold mb-2">
                글씨를 찾고 있어요
              </p>
              <p className="text-base text-amber-700">잠시만 기다려주세요...</p>
            </div>
          ) : (
            <>
              {/* 상단 안내 문구 */}

              {/* 에러 메시지 표시 영역 */}
              {error && (
                <div className="mb-4 bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              {/* 촬영 프레임: 클릭하여 카메라/갤러리 열기 */}
              <div
                className="bg-yellow-100 rounded-3xl p-12 mb-6 cursor-pointer hover:bg-yellow-200 transition-all"
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="text-center">
                  <Camera className="w-20 h-20 mx-auto text-amber-700 mb-4" />
                  <p className="text-2xl text-amber-900 font-bold mb-2">
                    여기를 눌러주세요
                  </p>
                  <p className="text-base text-amber-800">
                    사진을 찍거나 앨범에서 선택하세요
                  </p>
                </div>
              </div>

              {/* 하단 버튼들: 카메라, 갤러리 */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                {/* 카메라 버튼 */}
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="bg-yellow-100 hover:bg-yellow-200 rounded-3xl p-6 transition-all"
                >
                  <div className="text-center">
                    <Camera className="w-12 h-12 mx-auto text-amber-700 mb-3" />
                    <p className="text-base font-bold text-amber-900">
                      사진 촬영
                    </p>
                    <p className="text-xs text-amber-700 mt-1">
                      문서를 카메라로 찍어요
                    </p>
                  </div>
                </button>

                {/* 갤러리 버튼 */}
                <button
                  onClick={() => {
                    if (fileInputRef.current) {
                      fileInputRef.current.removeAttribute("capture");
                      fileInputRef.current.click();
                    }
                  }}
                  className="bg-yellow-100 hover:bg-yellow-200 rounded-3xl p-6 transition-all"
                >
                  <div className="text-center">
                    <Upload className="w-12 h-12 mx-auto text-amber-700 mb-3" />
                    <p className="text-base font-bold text-amber-900">
                      앨범에서 선택
                    </p>
                    <p className="text-xs text-amber-700 mt-1">
                      저장된 사진을 불러와요
                    </p>
                  </div>
                </button>
              </div>

              {/* 지난 기록 보기 버튼 */}
              <button
                onClick={() => router.push("/history")}
                className="w-full bg-yellow-100 hover:bg-yellow-200 rounded-3xl p-5 transition-all"
              >
                <div className="flex items-center justify-center gap-3">
                  <History className="w-7 h-7 text-amber-700" />
                  <span className="text-lg font-bold text-amber-900">
                    지난 기록 보기
                  </span>
                </div>
              </button>
            </>
          )}
        </div>

        {/* 숨겨진 파일 입력: 모바일 카메라 또는 갤러리 접근 */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          capture="environment" // 후면 카메라 우선
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>
    </div>
  );
}
