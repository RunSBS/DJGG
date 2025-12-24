// 파일명: CompanyChatbot.jsx
import React, { useState, useRef, useEffect } from "react";
import { FaComments, FaRobot, FaUser, FaPaperPlane, FaTimes } from "react-icons/fa";

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const chatLogRef = useRef(null);

    useEffect(() => {
        if (chatLogRef.current) {
            chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
        }
    }, [messages]);

    const appendMessage = (text, role) => {
        setMessages(prev => [...prev, { text, role }]);
    };

    const sendMessage = async () => {
        const msg = input.trim();
        if (!msg) return;

        appendMessage(msg, "user");
        setInput("");

        try {
            const resp = await fetch("/flask/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg }),
            });
            const data = await resp.json();

            if (!resp.ok) {
                appendMessage("봇 오류: " + (data.error || "알 수 없는 오류가 발생했습니다."), "bot");
                return;
            }
            appendMessage(data.answer, "bot");
        } catch {
            appendMessage("봇 오류: 서버에 연결할 수 없습니다.", "bot");
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") sendMessage();
    };

    return (
        <>
            <div
                className="chat-fab"
                title="전적/커뮤니티 챗봇 열기"
                onClick={() => setIsOpen(prev => !prev)}
                style={{
                    position: "fixed",
                    right: 24,
                    bottom: 24,
                    width: 64,
                    height: 64,
                    borderRadius: "50%",
                    backgroundColor: "#1e90ff",
                    color: "#fff",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    boxShadow: "0 4px 10px rgba(0,0,0,0.25)",
                    cursor: "pointer",
                    zIndex: 1000,
                }}
            >
                <FaComments size={28} />
            </div>

            {isOpen && (
                <div
                    className="chat-widget"
                    style={{
                        position: "fixed",
                        right: 24,
                        bottom: 100,
                        width: 380,
                        maxHeight: 520,
                        display: "flex",
                        flexDirection: "column",
                        borderRadius: 12,
                        overflow: "hidden",
                        boxShadow: "0 6px 16px rgba(0,0,0,0.35)",
                        backgroundColor: "#fff",
                        zIndex: 999,
                    }}
                >
                    <div
                        className="chat-widget-header"
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            padding: "10px 12px",
                            background: "linear-gradient(120deg, #1e90ff, #57a6ff)",
                            color: "#fff",
                        }}
                    >
                        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                            <div
                                className="chat-widget-avatar"
                                style={{
                                    width: 36,
                                    height: 36,
                                    borderRadius: "50%",
                                    backgroundColor: "rgba(255,255,255,0.15)",
                                    display: "flex",
                                    justifyContent: "center",
                                    alignItems: "center",
                                }}
                            >
                                <FaRobot />
                            </div>
                            <div>
                                <div style={{ fontSize: "0.95rem", fontWeight: "bold" }}>
                                    전적/커뮤니티 도우미
                                </div>
                                <div style={{ fontSize: "0.72rem", opacity: 0.95 }}>
                                    소환사 전적·커뮤니티 규정 관련 안내
                                </div>
                            </div>
                        </div>
                        <div
                            className="chat-widget-close"
                            style={{ cursor: "pointer" }}
                            onClick={() => setIsOpen(false)}
                        >
                            <FaTimes size={18} />
                        </div>
                    </div>

                    <div
                        id="chat-log"
                        ref={chatLogRef}
                        style={{
                            padding: 10,
                            height: 360,
                            overflowY: "auto",
                            backgroundColor: "#f7f9ff",
                        }}
                    >
                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`message ${msg.role}-message`}
                                style={{
                                    display: "flex",
                                    marginBottom: 8,
                                    flexDirection: msg.role === "user" ? "row-reverse" : "row",
                                }}
                            >
                                <div
                                    className="avatar"
                                    style={{
                                        width: 32,
                                        height: 32,
                                        borderRadius: "50%",
                                        display: "flex",
                                        justifyContent: "center",
                                        alignItems: "center",
                                        flexShrink: 0,
                                        fontSize: 16,
                                        backgroundColor: msg.role === "user" ? "#e8fff0" : "#eef6ff",
                                        color: msg.role === "user" ? "#006622" : "#0b4f9c",
                                    }}
                                >
                                    {msg.role === "user" ? <FaUser /> : <FaRobot />}
                                </div>
                                <div
                                    className="bubble"
                                    style={{
                                        maxWidth: "75%",
                                        padding: "8px 10px",
                                        borderRadius: 10,
                                        fontSize: "0.95rem",
                                        lineHeight: 1.4,
                                        marginLeft: msg.role === "user" ? 0 : 8,
                                        marginRight: msg.role === "user" ? 8 : 0,
                                        backgroundColor: msg.role === "user" ? "#e8fff0" : "#f0f6ff",
                                        color: msg.role === "user" ? "#004d1a" : "#002a55",
                                        whiteSpace: "pre-wrap",
                                    }}
                                >
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div
                        className="chat-widget-input"
                        style={{
                            padding: 8,
                            borderTop: "1px solid #ddd",
                            backgroundColor: "#fff",
                            display: "flex",
                            gap: 6,
                        }}
                    >
                        <input
                            type="text"
                            id="message"
                            placeholder="예시: 'Faker 전적 보여줘' 또는 '커뮤니티 신고 절차 알려줘'"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            style={{ flex: 1, padding: 8, fontSize: "0.95rem" }}
                        />
                        <button
                            id="send-btn"
                            onClick={sendMessage}
                            style={{
                                padding: "8px 12px",
                                fontSize: "0.9rem",
                                cursor: "pointer",
                                border: "none",
                                borderRadius: 6,
                                backgroundColor: "#1e90ff",
                                color: "#fff",
                                display: "flex",
                                alignItems: "center",
                                gap: 6,
                            }}
                        >
                            <FaPaperPlane size={14} />
                            전송
                        </button>
                    </div>

                    <div
                        className="chat-widget-footer-text"
                        style={{ fontSize: "0.72rem", color: "#666", padding: "6px 10px 10px 10px" }}
                    >
                        이 도우미는 플랫폼 문서(lol_docs.csv)에 등록된 내용만 바탕으로 안내합니다.
                        문서에 없는 질문에는 “이 플랫폼과 관련된 내용이 아니라 답변을 드릴 수 없습니다.”라고 응답합니다.
                    </div>
                </div>
            )}
        </>
    );
};

export default Chatbot;
