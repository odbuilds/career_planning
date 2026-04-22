const {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel,
  LevelFormat, BorderStyle, UnderlineType, PageNumber
} = require('/home/ubuntu/.nvm/versions/node/v24.11.0/lib/node_modules/docx');
const fs = require('fs');

const ACCENT = "1F4E79";   // dark navy for name
const HEADING_COLOR = "1F4E79";
const RULE_COLOR = "BFBFBF";
const BODY_SIZE = 20;       // 10pt
const SMALL_SIZE = 18;      // 9pt

function rule() {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE_COLOR } },
    spacing: { before: 0, after: 80 },
    children: []
  });
}

function sectionHeading(text) {
  return new Paragraph({
    spacing: { before: 220, after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE_COLOR } },
    children: [new TextRun({ text, bold: true, size: 22, color: HEADING_COLOR, font: "Arial", allCaps: true })]
  });
}

function jobTitle(role, company, dates) {
  return new Paragraph({
    spacing: { before: 160, after: 40 },
    children: [
      new TextRun({ text: role, bold: true, size: BODY_SIZE, font: "Arial" }),
      new TextRun({ text: " — " + company, bold: false, size: BODY_SIZE, font: "Arial" }),
      new TextRun({ text: "\t" + dates, italics: true, size: SMALL_SIZE, color: "595959", font: "Arial" })
    ],
    tabStops: [{ type: "right", position: 9350 }]
  });
}

function bullet(text, bold_prefix) {
  const children = [];
  if (bold_prefix) {
    children.push(new TextRun({ text: bold_prefix, bold: true, size: BODY_SIZE, font: "Arial" }));
    children.push(new TextRun({ text, size: BODY_SIZE, font: "Arial" }));
  } else {
    children.push(new TextRun({ text, size: BODY_SIZE, font: "Arial" }));
  }
  return new Paragraph({
    numbering: { reference: "bullet-list", level: 0 },
    spacing: { before: 40, after: 40 },
    children
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.before || 0, after: opts.after || 60 },
    children: [new TextRun({ text, size: BODY_SIZE, font: "Arial", italics: opts.italics || false })]
  });
}

function projectEntry(title, type, description) {
  return [
    new Paragraph({
      spacing: { before: 120, after: 30 },
      children: [
        new TextRun({ text: title, bold: true, size: BODY_SIZE, font: "Arial" }),
        new TextRun({ text: "  (" + type + ")", italics: true, size: SMALL_SIZE, color: "595959", font: "Arial" })
      ]
    }),
    new Paragraph({
      spacing: { before: 0, after: 60 },
      children: [new TextRun({ text: description, size: BODY_SIZE, font: "Arial" })]
    })
  ];
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 400, hanging: 260 } } }
        }]
      }
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: BODY_SIZE } } }
  },
  sections: [{
    properties: {
      page: { margin: { top: 1000, right: 1080, bottom: 1000, left: 1080 } }
    },
    children: [
      // Name
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "OLIVER DAY", bold: true, size: 52, color: ACCENT, font: "Arial" })]
      }),
      // Contact
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 40 },
        children: [new TextRun({ text: "oliver.p.day@gmail.com  |  +381 603388856  |  linkedin.com/in/dayoliver", size: SMALL_SIZE, color: "595959", font: "Arial" })]
      }),
      rule(),

      // Profile
      sectionHeading("Profile"),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        children: [new TextRun({
          text: "AI consultant with 10+ years delivering AI across enterprise clients in financial services, insurance, pharmaceutical, telecommunications, and property technology. Work spans the full consulting value chain: translating ambiguous business problems into implementable AI solutions, building and deploying production systems, designing evaluation frameworks that prove they work, and enabling client teams to operate and improve them independently. Equally at home in a scoping workshop with business stakeholders and in the technical implementation — which means fewer handoff failures and faster delivery. Track record of projects that generate measurable outcomes rather than proofs-of-concept that stall before production.",
          size: BODY_SIZE, font: "Arial"
        })]
      }),

      // Experience
      sectionHeading("Experience"),

      jobTitle("Conversational AI Developer", "HumanFirst", "November 2023 – Present"),
      new Paragraph({
        spacing: { before: 40, after: 60 },
        children: [new TextRun({
          text: "Delivered AI consulting engagements across insurance, financial services, telecommunications, property technology, and enterprise SaaS sectors — covering requirements analysis, solution architecture, build, evaluation, and client enablement.",
          size: BODY_SIZE, font: "Arial", italics: true, color: "404040"
        })]
      }),
      bullet("Designed and deployed an LLM-as-judge evaluation framework for a global insurance firm, automating quality monitoring of 50,000+ customer-broker conversations. Built prompt design, output validation, and human-baseline evaluation from scratch; results surfaced through BigQuery and Looker, replacing manual sampling with systematic coverage at scale."),
      bullet("Built a prompt orchestration and evaluation framework for an international mortgage brokerage enabling automated assessment of sales process adherence across 20 agents. Integrated with BigQuery/Looker so the client team could monitor and iterate on AI quality independently after handover."),
      bullet("Led the migration of a high-volume voice bot (100,000+ monthly contacts) from Dialogflow ES to CX. Ran HumanFirst clustering across 2 million customer utterances to restructure the NLU architecture, reducing intents from 950 to under 200 and improving F1 score from below 50% to 96%."),
      bullet("Conducted a structured evaluation of RAG solutions for a Canadian telecommunications firm, comparing LangChain, Dialogflow CX, Stack AI, and OpenAI GPTs across accuracy, hallucination rate, implementation complexity, and cost. Delivered platform-specific implementation guides and a strategic recommendation for a large-scale contact centre deployment."),
      bullet("Applied GPT-4 to analyse 20,000+ customer reviews across four competitors for an online marketplace, building a hierarchical taxonomy of issues and mapping findings against business objectives. Delivered interactive Plotly visualisations for stakeholder presentation."),
      bullet("Led a strategic proof-of-concept for a Canadian parcel delivery firm evaluating Microsoft Copilot with Azure CLU. Analysed 10,000 customer service conversations to generate intent taxonomies and automated flow designs; delivered a technical risk assessment covering RAG limitations within four weeks."),
      bullet("Executed a rapid POC for a Latin American call centre, analysing 20,000+ conversations to classify sales objections and successful response strategies. Delivered actionable methodology within one week, enabling the client to implement independently."),
      bullet("Processed 50,000+ customer conversations for a European CPaaS provider to generate a structured FAQ knowledge base optimised for RAG implementation, pairing problem descriptions with step-by-step resolution guides."),
      bullet("Designed and delivered a two-month generative AI training programme for a Canadian engineering firm, transforming 40 non-technical business users into active AI practitioners. Achieved 60%+ adoption with participants independently implementing use cases across marketing, operations, and process improvement."),
      bullet("Designed and built a production LLM pipeline for internal product development: scraped and qualified 15,000+ LinkedIn profiles, generated personalised outreach at scale with A/B testing, and produced 20+ qualified demo calls per week — replacing a sales team function."),

      jobTitle("Conversation Engineer", "Conversation Design Institute Services", "October 2021 – October 2023"),
      bullet("Consulted on conversational AI strategy, platform selection, and NLU implementation for enterprise clients in financial services and pharmaceutical sectors — from initial scoping through deployment and ongoing improvement."),
      bullet("Designed a structured consulting methodology for conversational AI platform evaluation — mapping client technical requirements, interaction complexity, and operational context to platform capabilities across leading providers."),
      bullet("Led R&D for CDI's LLM consulting offering — researching emerging LLM capabilities, building POC implementations, and packaging findings into structured consulting products for enterprise clients."),
      bullet("Led NLU model improvement programmes for financial services and pharmaceutical clients — systematic analysis of production conversation data driving measurable quality improvements."),
      bullet("Designed and delivered client-facing workshops on NLU evaluation, LLM capabilities, conversation design, and AI adoption strategy."),

      jobTitle("Conversation Designer", "Travtus", "July 2021 – April 2023"),
      bullet("Designed and built conversational AI experiences for a property management platform, covering the full tenant and landlord interaction lifecycle at scale."),

      // Capabilities
      sectionHeading("Capabilities"),
      bullet("AI solution scoping and architecture — requirements translation, feasibility assessment, platform selection, build-vs-buy analysis"),
      bullet("Client delivery — end-to-end project ownership from discovery through deployment and team enablement"),
      bullet("LLM evaluation design — LLM-as-judge frameworks, human-baseline validation, prompt optimisation pipelines"),
      bullet("Conversational AI design and deployment — Dialogflow ES/CX, Kore.AI, Microsoft Copilot Studio, Azure CLU"),
      bullet("NLU model development and optimisation — intent architecture, clustering-based simplification, F1 improvement"),
      bullet("Agentic workflow development — LangGraph, n8n, multi-step LLM pipelines, prompt-first methodology"),
      bullet("RAG solution design and evaluation"),
      bullet("Enterprise AI training and enablement — workshop design and delivery, adoption programme development"),
      bullet("Cross-sector experience — insurance, financial services, pharmaceutical, telecommunications, property technology, enterprise SaaS"),

      // Education
      sectionHeading("Education"),
      new Paragraph({
        spacing: { before: 80, after: 20 },
        children: [
          new TextRun({ text: "Knox College", bold: true, size: BODY_SIZE, font: "Arial" }),
          new TextRun({ text: ", Galesburg, Illinois — Bachelor of Arts, Political Science and Biology, 2005", size: BODY_SIZE, font: "Arial" })
        ]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        children: [
          new TextRun({ text: "London School of Commerce", bold: true, size: BODY_SIZE, font: "Arial" }),
          new TextRun({ text: ", Belgrade, Serbia — MBA with Distinction, 2013", size: BODY_SIZE, font: "Arial" })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/home/ubuntu/source/career_planning/cvs/cv_ai_consulting.docx", buffer);
  console.log("Done: cv_ai_consulting.docx");
});
