from dataclasses import dataclass

from typetemp.template.typed_template import TypedTemplate

class PragmaticStarterKitBook:
    """
    Represents the book "How the PragmaticProgrammerAGIAgent built the Pragmatic Starter Kit with DDD, Docker Compose,
    Git Actions, Pytest, etc" and provides a summary of its 20 chapters.
    """

    def __init__(self):
        self.title = "How the PragmaticProgrammerAGIAgent built the Pragmatic Starter Kit with DDD, Docker Compose, Git Actions, Pytest, etc"
        self.chapters = [
            {
                "title": "Introduction to PragmaticProgrammerAGIAgent",
                "summary": "An introduction to the innovative PragmaticProgrammerAGIAgent and its mission to create high-quality code."
            },
            {
                "title": "The Pragmatic Philosophy",
                "summary": "A look into the Pragmatic Programmer's approach that drives the AGIAgent."
            },
            {
                "title": "DDD and Code Generation",
                "summary": "Exploring Domain-Driven Design principles and how AGIAgent integrates them."
            },
            {
                "title": "Automated Testing with Pytest",
                "summary": "How AGIAgent employs Pytest for robust and automated code testing."
            },
            {
                "title": "Docker Compose for Environment Management",
                "summary": "Utilizing Docker Compose for controlling and managing development environments."
            },
            {
                "title": "Continuous Integration with Git Actions",
                "summary": "Implementing Continuous Integration workflows using Git Actions."
            },
            {
                "title": "Refinement and Iteration in Code Generation",
                "summary": "The iterative process of code generation and refinement used by AGIAgent."
            },
            {
                "title": "Version Control Strategies",
                "summary": "Effective version control practices followed by AGIAgent."
            },
            {
                "title": "Building the Pragmatic Starter Kit",
                "summary": "A deep dive into building the Pragmatic Starter Kit using various technologies."
            },
            {
                "title": "Regression Testing and Full Automation",
                "summary": "Implementing regression testing and achieving full automation in development."
            },
            {
                "title": "Monitoring and Performance Optimization",
                "summary": "Methods used by AGIAgent to monitor and optimize performance."
            },
            {
                "title": "Documentation and Community Engagement",
                "summary": "Creating comprehensive documentation and fostering community collaboration."
            },
            {
                "title": "Security and Compliance",
                "summary": "Ensuring security measures and compliance with legal requirements."
            },
            {
                "title": "Deployment and Scalability",
                "summary": "Strategies for deploying and scaling applications effectively."
            },
            {
                "title": "Debugging and Troubleshooting",
                "summary": "Advanced techniques for debugging and troubleshooting code."
            },
            {
                "title": "Customizing the Pragmatic Starter Kit",
                "summary": "Guidelines for customizing and extending the Pragmatic Starter Kit."
            },
            {
                "title": "Real-world Case Studies",
                "summary": "A look at how the Pragmatic Starter Kit has been applied in real-world scenarios."
            },
            {
                "title": "Future Directions and Evolution",
                "summary": "Exploring potential future enhancements and the evolution of the Pragmatic Starter Kit."
            },
            {
                "title": "Contributing to the Project",
                "summary": "How to contribute to the ongoing development and improvement of the Pragmatic Starter Kit."
            },
            {
                "title": "Conclusion: Building a Pragmatic Future",
                "summary": "Reflecting on the journey and envisioning a pragmatic future with AGIAgent."
            },
        ]

    def get_chapter_summaries(self):
        """
        Returns markdown formatted summaries of all 20 chapters.

        Returns:
            str: The markdown formatted chapter summaries.
        """
        summaries_md = ""
        for idx, chapter in enumerate(self.chapters, start=1):
            summaries_md += f"### Chapter {idx}: {chapter['title']}\n\n{chapter['summary']}\n\n"
        return summaries_md

# Instantiate the PragmaticStarterKitBook class
book = PragmaticStarterKitBook()

# Print the markdown formatted summaries of all 20 chapters
print(book.get_chapter_summaries())


@dataclass
class ChapterTemplate(TypedTemplate):
    chapter_number: int = 0
    chapter_title: str = ""
    summary: str = ""
    to: str = "./chapters/Chapter{{ chapter_number }}.py"
    source = """
class Chapter{{ chapter_number }}:
    \"\"\"{{ chapter_title }}

    {{ summary }}
    \"\"\"
    def __init__(self):
        self.title = "{{ chapter_title }}"
        self.summary = "{{ summary }}"
    """


def generate_chapters(chapters):
    # Define and generate the chapter classes
    for idx, chapter in enumerate(chapters):
        chapter_template = ChapterTemplate(
            chapter_number=idx + 1,
            chapter_title=chapter["title"],
            summary=chapter["summary"]
        )
        chapter_template.render()

    print("Chapters generated successfully.")


generate_chapters(PragmaticStarterKitBook().chapters)

