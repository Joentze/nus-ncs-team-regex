"use client";
import Image from "next/image";
import { QueryClient, QueryClientProvider } from "react-query";
import {
  AppShell,
  Burger,
  Group,
  MantineProvider,
  Skeleton,
  Text,
  useMantineTheme,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import SideBar from "./components/SideBar/SideBar";
import { ConversationProvider } from "./customHooks/conversationHooks";
import MainChat from "./components/MainChat/MainChat";

const queryClient = new QueryClient();

export default function Home() {
  const [opened, { toggle }] = useDisclosure();

  return (
    <main>
      <QueryClientProvider client={queryClient}>
        <ConversationProvider>
          <AppShell
            header={{ height: 60 }}
            navbar={{
              width: 300,
              breakpoint: "sm",
              collapsed: { mobile: !opened },
            }}
            padding="md"
          >
            <AppShell.Header>
              <Group h="100%" px="md">
                <Text fw={700} size="lg">
                  Govtech ChatGPT 🇸🇬
                </Text>
              </Group>
            </AppShell.Header>
            <SideBar />
            <AppShell.Main>
              <MainChat />
            </AppShell.Main>
          </AppShell>
        </ConversationProvider>
      </QueryClientProvider>
    </main>
  );
}
