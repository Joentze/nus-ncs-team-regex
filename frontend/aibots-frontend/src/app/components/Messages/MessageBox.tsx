import { QueryRole } from "@/restHelpers/conversationHelper";
import { Flex, Text, Divider } from "@mantine/core";

interface IMessageBox {
  role: QueryRole;
  content: string;
}

const MessageBox: React.FC<IMessageBox> = ({ role, content }) => {
  return (
    <Flex direction={"column"} my={24}>
      <Divider mb={4}></Divider>
      {role === "user" ? (
        <>
          <Text
            fw={700}
            size="xl"
            ta={"right"}
            variant="gradient"
          >{`${role}:`}</Text>
          <Text fw={500} ta={"right"}>
            {content}
          </Text>
        </>
      ) : (
        <>
          <Text fw={600} size="xl" c="blue">{`${role} 🤖:`}</Text>
          <Text fs={"italic"}>{content}</Text>
        </>
      )}
    </Flex>
  );
};
export default MessageBox;
