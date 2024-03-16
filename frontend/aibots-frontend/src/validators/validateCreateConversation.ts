export const validateCreateConversation = (
  conversationName: string,
  conversationParams: string
): void => {
  if (conversationName === undefined || conversationName === "")
    throw new Error("The conversation name cannot be blank!");
  JSON.parse(conversationParams);
};
