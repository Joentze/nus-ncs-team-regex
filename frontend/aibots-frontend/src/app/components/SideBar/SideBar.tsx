import { getAllConversations } from "@/restHelpers/conversationHelper";
import {
  ActionIcon,
  AppShell,
  Button,
  Divider,
  Flex,
  Skeleton,
  Text,
} from "@mantine/core";
import { IoAdd, IoReload } from "react-icons/io5";
import { useEffect } from "react";
import { useQuery } from "react-query";
import { useConversation } from "@/app/customHooks/conversationHooks";
import CreateConvoPopup from "../Modal/CreateConvoPopup";

const SideBar = () => {
  const { conversationId, setConversationId } = useConversation();
  const { isLoading, error, data, refetch } = useQuery({
    queryKey: ["convoAll"],
    queryFn: getAllConversations,
  });
  const setConv = (convoId: string) => {
    setConversationId(convoId);
  };
  useEffect(() => {
    refetch();
  }, [conversationId]);
  return (
    <AppShell.Navbar p="md">
      <CreateConvoPopup />
      <Divider mt={8} />
      <Flex>
        <Text mt={8} fw={500} w={"100%"} c={"gray"}>
          Conversations 💬
        </Text>
        <ActionIcon mt={5} variant="subtle" onClick={() => refetch()}>
          <IoReload />
        </ActionIcon>
      </Flex>
      {data?.data.map((item, index) => {
        return (
          <>
            <Button
              fullWidth
              mt={8}
              variant={item._id === conversationId ? "light" : "subtle"}
              key={item._id}
              onClick={() => setConv(item._id)}
            >
              {item.name}
            </Button>
            <Divider mt={8}></Divider>
          </>
        );
      })}
    </AppShell.Navbar>
  );
};

export default SideBar;
