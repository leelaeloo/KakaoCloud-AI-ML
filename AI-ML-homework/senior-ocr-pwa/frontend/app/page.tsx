"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Camera, FileText, Pill, Newspaper, History } from "lucide-react";
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
    // HTTPS 환경에서는 navigator.clipboard 사용
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard
        .writeText(text)
        .then(() => alert("복사되었습니다!"))
        .catch(() => fallbackCopy(text));
    } else {
      // HTTP 환경에서는 fallback 방식 사용
      fallbackCopy(text);
    }
  };

  const fallbackCopy = (text: string) => {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand("copy");
      alert("복사되었습니다!");
    } catch (err) {
      alert("복사에 실패했습니다. 직접 선택해서 복사해주세요.");
    }
    document.body.removeChild(textArea);
  };

  // 결과 화면 (OCR 완료 후)
  if (result) {
    return (
      <div className="min-h-screen bg-white">
        {/* 통합 헤더 (모바일/데스크톱 공통) */}
        <header className="bg-yellow-100 shadow-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8 py-4">
            <div className="flex items-center justify-between">
              <button
                onClick={() => router.push("/")}
                className="flex items-center gap-3 hover:opacity-80 transition-opacity"
              >
                <span className="text-3xl md:text-4xl leading-none">📖</span>
                <h1 className="text-2xl md:text-3xl font-bold text-gray-900 leading-none">
                  읽어드림
                </h1>
              </button>
              <button
                onClick={() => router.push("/history")}
                className="bg-white hover:bg-gray-50 text-gray-900 font-bold px-4 py-2 md:px-6 md:py-3 rounded-xl transition-all flex items-center gap-2 shadow-md"
              >
                <History className="w-4 h-4 md:w-5 md:h-5" />
                <span className="hidden sm:inline">히스토리</span>
              </button>
            </div>
          </div>
        </header>

        <div className="max-w-md mx-auto md:max-w-4xl px-4 py-6 md:py-8">
          {/* 결과 카드: OCR 텍스트 표시 영역 */}
          <div className="card md:shadow-2xl ">
            {/* 헤더 */}
            <div className="mb-4 sm:mb-6 pb-4 sm:pb-6 ">
              <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 text-center mb-3">
                읽어드림
              </h1>
              <p className="text-lg sm:text-xl text-gray-700 font-medium text-center">
                ✅ 글씨를 찾았어요!
              </p>
            </div>

            <p className="text-base sm:text-lg text-gray-600 font-medium mb-4 sm:mb-6 text-center leading-relaxed">
              아래 내용을 확인해주세요
            </p>

            {/* 결과 텍스트 박스: 스크롤 가능, 최대 높이 40vh */}
            <div className="bg-yellow-100 rounded-3xl p-6 mb-6 max-h-[40vh] overflow-auto ">
              <p className="text-xl leading-relaxed ocr-text text-gray-900">
                {result.text || "글씨를 찾을 수 없어요"}
              </p>
            </div>

            {/* 상세 정보: 단어 수, 정확도 표시 */}
            <div className="bg-yellow-100 rounded-3xl p-5 mb-6 space-y-3 ">
              <div className="flex justify-between py-2">
                <span className="text-gray-700 text-base font-medium">
                  글자 개수
                </span>
                <span className="font-bold text-gray-900 text-lg">
                  {result.word_count}개
                </span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-gray-700 text-base font-medium">
                  정확도
                </span>
                <span className="font-bold text-gray-900 text-lg">
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
                  : "bg-yellow-100 hover:bg-yellow-200 text-gray-900 "
              }`}
            >
              {isSpeaking ? "⏹️ 소리 멈추기" : "🔊 소리로 읽어주기"}
            </button>
            <p className="text-sm text-gray-700 text-center mb-6">
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
                className="bg-gray-100 hover:bg-gray-200 rounded-3xl p-5 transition-all"
              >
                <div className="text-center">
                  <p className="text-lg font-bold text-gray-900">
                    🔄 다시 찍기
                  </p>
                  <p className="text-xs text-gray-700 mt-1">
                    처음으로 돌아가요
                  </p>
                </div>
              </button>

              <button
                onClick={() => copyToClipboard(result.text)}
                className="bg-gray-100 hover:bg-gray-200 rounded-3xl p-5 transition-all"
              >
                <div className="text-center">
                  <p className="text-lg font-bold text-gray-900">📋 복사하기</p>
                  <p className="text-xs text-gray-700 mt-1">
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
    <div className="min-h-screen bg-white">
      {/* PC 헤더 */}
      <header className="hidden md:block bg-yellow-100 shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-8">
              <button
                onClick={() => router.push("/")}
                className="flex items-center gap-3 hover:opacity-80 transition-opacity"
              >
                <span className="text-3xl leading-none">📖</span>
                <h1 className="text-2xl font-bold text-gray-900 leading-none">읽어드림</h1>
              </button>

              {/* PC 메뉴 */}
              <nav className="flex items-center gap-6">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="text-gray-700 hover:text-gray-900 font-medium transition-all"
                >
                  약봉투
                </button>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="text-gray-700 hover:text-gray-900 font-medium transition-all"
                >
                  일반문서
                </button>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="text-gray-700 hover:text-gray-900 font-medium transition-all"
                >
                  신문/책
                </button>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="text-gray-700 hover:text-gray-900 font-medium transition-all"
                >
                  사진촬영
                </button>
              </nav>
            </div>

            <button
              onClick={() => router.push("/history")}
              className="bg-white hover:bg-gray-50 text-gray-900 font-bold px-6 py-3 rounded-xl transition-all flex items-center gap-2 shadow-md"
            >
              <History className="w-5 h-5" />
              히스토리
            </button>
          </div>
        </div>
      </header>

      {/* 모바일 헤더 */}
      <header className="md:hidden bg-yellow-100 shadow-md sticky top-0 z-50">
        <div className="px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.push("/")}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity"
            >
              <span className="text-3xl leading-none">📖</span>
              <h1 className="text-2xl font-bold text-gray-900 leading-none">읽어드림</h1>
            </button>
            <button
              onClick={() => router.push("/history")}
              className="bg-white hover:bg-gray-50 text-gray-900 font-bold px-4 py-2 rounded-xl transition-all flex items-center gap-2 shadow-md"
            >
              <History className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* 메인 컨텐츠 영역 */}
      <div className="max-w-md mx-auto md:max-w-7xl px-4 py-6 md:py-12">
        {/* 데스크톱: 좌우 분할 레이아웃 / 모바일: 세로 레이아웃 */}
        <div className="md:grid md:grid-cols-2 md:gap-12 md:items-start">
          {/* 왼쪽: 히어로 섹션 (데스크톱만) */}
          <div className="hidden md:block">
            <div className="sticky top-24">
              <h2 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
                어르신을 위한
                <br />
                문서 읽어주기
                <br />
                서비스
              </h2>
              <p className="text-xl text-gray-700 mb-8 leading-relaxed">
                사진을 찍으면 글씨를 크게 보여드리고
                <br />
                소리로 읽어드립니다.
              </p>
              <div className="space-y-4 text-lg text-gray-600">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">📷</span>
                  <span>카메라로 문서 촬영</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl">🔍</span>
                  <span>텍스트 자동 인식</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl">📖</span>
                  <span>큰 글씨로 표시</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl">🔊</span>
                  <span>음성으로 읽어주기</span>
                </div>
              </div>
            </div>
          </div>

          {/* 오른쪽: 촬영 카드 */}
          <div className="card md:shadow-2xl ">
            {/* 데스크톱 헤더 */}
            <div className="hidden md:block mb-6 pb-6 ">
              <h2 className="text-3xl font-bold text-gray-900 text-center mb-2">
                시작하기
              </h2>
              <p className="text-lg text-gray-600 text-center">
                읽고 싶은 문서 종류를 선택해주세요
              </p>
            </div>

            {isProcessing ? (
              // 로딩 스피너
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-yellow-300 mb-6"></div>
                <p className="text-xl text-gray-900 font-bold mb-2">
                  글씨를 찾고 있어요
                </p>
                <p className="text-base text-gray-600">
                  잠시만 기다려주세요...
                </p>
              </div>
            ) : (
              <>
                {/* 에러 메시지 표시 영역 */}
                {error && (
                  <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4 rounded">
                    <p className="text-red-800">{error}</p>
                  </div>
                )}

                {/* 문서 타입 선택 버튼들: 2x2 그리드 */}
                <div className="grid grid-cols-2 gap-2 sm:gap-4 mb-3 sm:mb-4">
                  {/* 약봉투 버튼 */}
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="aspect-square bg-yellow-100 hover:bg-yellow-200 rounded-2xl sm:rounded-3xl p-2 sm:p-4 transition-all shadow-md hover:shadow-lg "
                  >
                    <div className="flex flex-col items-center justify-center h-full gap-1 sm:gap-2">
                      <Pill className="w-10 h-10 sm:w-14 sm:h-14 text-gray-900" />
                      <div className="text-center">
                        <p className="text-base sm:text-lg font-bold text-gray-900 leading-tight">
                          약봉투
                        </p>
                        <p className="text-[10px] sm:text-xs text-gray-700 leading-tight whitespace-nowrap">
                          약 설명서
                        </p>
                      </div>
                    </div>
                  </button>

                  {/* 일반 문서 버튼 */}
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="aspect-square bg-yellow-100 hover:bg-yellow-200 rounded-2xl sm:rounded-3xl p-2 sm:p-4 transition-all shadow-md hover:shadow-lg "
                  >
                    <div className="flex flex-col items-center justify-center h-full gap-1 sm:gap-2">
                      <FileText className="w-10 h-10 sm:w-14 sm:h-14 text-gray-900" />
                      <div className="text-center">
                        <p className="text-base sm:text-lg font-bold text-gray-900 leading-tight">
                          일반 문서
                        </p>
                        <p className="text-[10px] sm:text-xs text-gray-700 leading-tight whitespace-nowrap">
                          서류, 편지
                        </p>
                      </div>
                    </div>
                  </button>

                  {/* 신문/책 버튼 */}
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="aspect-square bg-yellow-100 hover:bg-yellow-200 rounded-2xl sm:rounded-3xl p-2 sm:p-4 transition-all shadow-md hover:shadow-lg "
                  >
                    <div className="flex flex-col items-center justify-center h-full gap-1 sm:gap-2">
                      <Newspaper className="w-10 h-10 sm:w-14 sm:h-14 text-gray-900" />
                      <div className="text-center">
                        <p className="text-base sm:text-lg font-bold text-gray-900 leading-tight">
                          신문/책
                        </p>
                        <p className="text-[10px] sm:text-xs text-gray-700 leading-tight whitespace-nowrap">
                          기사, 책
                        </p>
                      </div>
                    </div>
                  </button>

                  {/* 사진 촬영 버튼 */}
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="aspect-square bg-yellow-100 hover:bg-yellow-200 rounded-2xl sm:rounded-3xl p-2 sm:p-4 transition-all shadow-md hover:shadow-lg "
                  >
                    <div className="flex flex-col items-center justify-center h-full gap-1 sm:gap-2">
                      <Camera className="w-10 h-10 sm:w-14 sm:h-14 text-gray-900" />
                      <div className="text-center">
                        <p className="text-base sm:text-lg font-bold text-gray-900 leading-tight">
                          사진 촬영
                        </p>
                        <p className="text-[10px] sm:text-xs text-gray-700 leading-tight whitespace-nowrap">
                          직접 촬영
                        </p>
                      </div>
                    </div>
                  </button>
                </div>

                {/* 지난 기록 보기 버튼 (모바일만) */}
                <button
                  onClick={() => router.push("/history")}
                  className="w-full bg-gray-100 hover:bg-gray-200 rounded-2xl sm:rounded-3xl p-3 sm:p-4 transition-all md:hidden "
                >
                  <div className="flex items-center justify-center gap-2 sm:gap-3">
                    <History className="w-6 h-6 sm:w-7 sm:h-7 text-gray-700" />
                    <span className="text-base sm:text-lg font-bold text-gray-900">
                      지난 기록 보기
                    </span>
                  </div>
                </button>
              </>
            )}
          </div>
        </div>
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
  );
}
