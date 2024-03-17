import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, Input, JsonInput, ActionIcon } from "@mantine/core";
import { IoAdd, IoCog } from "react-icons/io5";
import { useEffect, useState } from "react";
import { useConversation } from "@/app/customHooks/conversationHooks";
import { validateCreateConversation } from "@/validators/validateCreateConversation";
import {
  editConversation,
  getFullConversation,
} from "@/restHelpers/conversationHelper";

const EditConvoPopup = () => {
  const { conversationId, setConversationId } = useConversation();
  const [loading, setLoading] = useState<boolean>(false);
  const [opened, { open, close }] = useDisclosure(false);
  const [conversationName, setConversationName] = useState<string>("");
  const [jsonValue, setJsonValue] = useState<string>(JSON.stringify(""));

  useEffect(() => {
    const getConversationDetails = async () => {
      const { name, params } = await getFullConversation(conversationId);
      setConversationName(name);
      setJsonValue(JSON.stringify(params));
    };
    getConversationDetails();
  }, [conversationId]);

  const editConvo = async () => {
    try {
      validateCreateConversation(conversationName, jsonValue);
      setLoading(true);
      await editConversation(conversationId, {
        name: conversationName,
        params: JSON.parse(jsonValue),
      });
      setLoading(false);
    } catch (e) {
      alert(e);
    }
  };
  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        title="Edit Conversation Settings 📝"
      >
        <Modal.Body>
          <Input.Wrapper
            label="Rename Conversation"
            description="Edit your conversation name to suit your task better!"
          >
            <Input
              defaultValue={conversationName}
              value={conversationName}
              placeholder="Example: an Exploration into Large Language Models"
              onChange={(event) => setConversationName(event.target.value)}
            />
          </Input.Wrapper>
          <br></br>

          <Input.Wrapper
            label="Conversation Parameters"
            description="Set OpenAI chat parameters"
          >
            <JsonInput
              defaultValue={jsonValue}
              value={jsonValue}
              onChange={setJsonValue}
              mt={8}
            />
          </Input.Wrapper>
          <br></br>
          <Button
            loading={loading}
            loaderProps={{ type: "dots" }}
            fullWidth
            onClick={async () => {
              await editConvo();
              close();
            }}
          >
            Confirm
          </Button>
        </Modal.Body>
      </Modal>

      <ActionIcon size={"lg"} variant="light" onClick={open}>
        <IoCog size={"md"} />
      </ActionIcon>
    </>
  );
};

export default EditConvoPopup;
