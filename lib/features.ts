import {
  FileText,
  MessageSquare,
  ShieldCheck,
} from "lucide-react";

export const features = [
  {
    title: "Upload Documents",
    description:
      "Build your private knowledge base by uploading PDFs, documents, and other files.",
    link: "#",
    icon: FileText,
  },
  {
    title: "Ask Questions",
    description:
      "Ask natural language questions and let AI find the most relevant information.",
    link: "/chat",
    icon: MessageSquare,
  },
  {
    title: "Get Reliable Answers",
    description:
      "Receive answers grounded in your documents with relevant sources and citations.",
    link: "/",
    icon: ShieldCheck,
  },
];