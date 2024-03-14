import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, Input, JsonInput } from "@mantine/core";
import { IoAdd } from "react-icons/io5";
import { useState } from "react";
import { useConversation } from "@/app/customHooks/conversationHooks";
import { validateCreateConversation } from "@/validators/validateCreateConversation";
import { createConversation } from "@/restHelpers/conversationHelper";

const defaultParams = {
  model: "gpt-4",
};

const CreateConvoPopup = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const { conversationId, setConversationId } = useConversation();
  const [opened, { open, close }] = useDisclosure(false);
  const [conversationName, setConversationName] = useState<string>("");
  const [jsonValue, setJsonValue] = useState(JSON.stringify(defaultParams));
  const createConvo = async () => {
    try {
      validateCreateConversation(conversationName, jsonValue);
      setLoading(true);
      const { id } = await createConversation({
        name: conversationName,
        params: JSON.parse(jsonValue),
        tokens: 0,
      });
      setLoading(false);
      setConversationId(id);
    } catch (e) {
      alert(e);
    }
  };
  return (
    <>
      <Modal opened={opened} onClose={close} title="Create a Conversation 📝">
        <Modal.Body>
          <Input.Wrapper
            label="Conversation Name"
            description="Organise your conversations by giving it a unique name!"
          >
            <Input
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
            <JsonInput value={jsonValue} onChange={setJsonValue} mt={8} />
          </Input.Wrapper>
          <br></br>
          <Button
            fullWidth
            onClick={async () => {
              await createConvo();
              close();
            }}
          >
            Create!
          </Button>
        </Modal.Body>
      </Modal>

      <Button
        leftSection={<IoAdd />}
        onClick={open}
        loading={loading}
        loaderProps={{ type: "dots" }}
      >
        Add Conversation
      </Button>
    </>
  );
};

export default CreateConvoPopup;
