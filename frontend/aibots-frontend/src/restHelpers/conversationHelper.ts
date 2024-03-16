import axios from "axios";

const API_ENDPOINT = process.env.NEXT_PUBLIC_API_ENDPOINT;

export enum QueryRole {
  USER = "user",
  SYSTEM = "system",
  FUNCTION = "function",
  ASSISTANT = "assistant",
}

export interface Prompt {
  role: QueryRole;
  content: string;
}

export interface Conversation {
  _id: string;
  name: string;
  params: object;
  tokens: number;
}

export interface CreateConversationBody {
  name: string;
  params: object;
  tokens: number;
}

export interface EditConversationBody {
  name: string;
  params: object;
}

export interface AllConversationsResponse {
  data: Conversation[];
}

export interface ConversationFull extends Conversation {
  messages: Prompt[];
}

export interface CreatedResponse {
  id: string;
}

export const getAllConversations =
  async (): Promise<AllConversationsResponse> => {
    try {
      const response = await axios.get(`${API_ENDPOINT}/conversations`);
      return response.data as AllConversationsResponse;
    } catch (e) {
      throw new Error(e as string);
    }
  };

export const getFullConversation = async (
  conversationId: string
): Promise<ConversationFull> => {
  try {
    const response = await axios.get(
      `${API_ENDPOINT}/conversations/${conversationId}`
    );
    return response.data as ConversationFull;
  } catch (e) {
    throw new Error(e as string);
  }
};

export const createConversation = async (
  convoBody: CreateConversationBody
): Promise<CreatedResponse> => {
  try {
    const response = await axios.post(
      `${API_ENDPOINT}/conversations`,
      convoBody
    );
    const { data } = response;
    return data as CreatedResponse;
  } catch (e) {
    throw new Error(e as string);
  }
};

export const postQuery = async (
  conversationId: string,
  query: Prompt
): Promise<CreatedResponse> => {
  try {
    const response = await axios.post(
      `${API_ENDPOINT}/queries?id=${conversationId}`,
      query
    );
    const { data } = response;
    console.log(data);
    return data as CreatedResponse;
  } catch (e) {
    throw new Error(e as string);
  }
};

export const editConversation = async (
  conversationId: string,
  convoBody: EditConversationBody
): Promise<void> => {
  try {
    const response = await axios.put(
      `${API_ENDPOINT}/conversations/${conversationId}`,
      convoBody
    );
  } catch (e) {
    throw new Error(e as string);
  }
};
