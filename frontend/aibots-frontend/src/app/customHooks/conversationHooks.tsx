import React, {
  useContext,
  useState,
  createContext,
  FunctionComponent,
} from "react";

//define the type of the context
interface ConversationContextProps {
  conversationId: string;
  setConversationId: (id: string) => void;
}

// create the context
const ConversationContext = createContext<ConversationContextProps | undefined>(
  undefined
);

export const ConversationProvider: React.FC<any> = ({ children }) => {
  const [conversationId, setConversationId] = useState<string>("");

  // value to pass to ConversationProvider
  const value = { conversationId, setConversationId };

  return (
    <ConversationContext.Provider value={value}>
      {children}
    </ConversationContext.Provider>
  );
};

// Hook to make it easy to use the context
export const useConversation = () => {
  const context = useContext(ConversationContext);
  if (context === undefined) {
    throw new Error(
      "useConversation must be used within a ConversationProvider"
    );
  }
  return context;
};
