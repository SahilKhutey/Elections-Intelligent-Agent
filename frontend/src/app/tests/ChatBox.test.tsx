import { render, screen, fireEvent } from "@testing-library/react";
import ChatBox from "../components/ChatBox";

describe("ChatBox Component", () => {
  const mockProps = {
    chat: [],
    loading: false,
    query: "",
    setQuery: jest.fn(),
    handleSend: jest.fn(),
    placeholder: "Ask about voting...",
    aiThinking: "Thinking...",
    location: "India"
  };

  test("renders empty state correctly", () => {
    render(<ChatBox {...mockProps} />);
    expect(screen.getByText(/How can I help you today?/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Ask about voting.../i)).toBeInTheDocument();
  });

  test("calls setQuery on input change", () => {
    render(<ChatBox {...mockProps} />);
    const input = screen.getByPlaceholderText(/Ask about voting.../i);
    fireEvent.change(input, { target: { value: "How to vote?" } });
    expect(mockProps.setQuery).toHaveBeenCalledWith("How to vote?");
  });

  test("displays loading state", () => {
    render(<ChatBox {...mockProps} loading={true} />);
    expect(screen.getByText(/Thinking.../i)).toBeInTheDocument();
  });

  test("renders messages when chat array is not empty", () => {
    const chatWithMessages = [
      { role: 'user' as const, content: 'Hello' },
      { role: 'ai' as const, content: 'Hi there!' }
    ];
    render(<ChatBox {...mockProps} chat={chatWithMessages} />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
    expect(screen.getByText('Hi there!')).toBeInTheDocument();
  });
});
