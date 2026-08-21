---
name: kb-quiz
description: Quiz the user about topics from the knowledge base.
---

Ask questions about a topic selected from the knowledge base (usually a specific note or set of notes). Use the information about sources from the frontmatter to gather any additional necessary context, e.g. from source code.

Ask 1-2 questions per note. The questions should focus on reasoning and understanding the topic, not on plain recall - recall is handled by flashcards (if the knowledge base has flashcards related to the notes, you can skip facts covered by the flashcards). Be careful not to give away the answers in the questions. Also, try to formulate the questions so that the answer doesn't have to be a long elaborate. If there are any logs of previous quizzes on the topic, ask about the aspects that haven't been covered yet or that the user failed to answer properly last time.

If you have access to the sources, you can expand the scope of the questions slightly to cover adjacent, related issues. If the user provides information that wasn't previously available in the quizzed item, take that part of his answer and append it to the corresponding raw capture.

After the quiz is done, log the questions, answers, and any important comments on the answers in a file.
