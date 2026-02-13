from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage


class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self, llm):
        self.llm = llm

    # ---------------------------------------------------------
    # TITLE CREATION
    # ---------------------------------------------------------
    def title_creation(self, state: BlogState):
        """
        Create the title for the blog
        """

        if "topic" in state and state["topic"]:

            prompt = f"""
            You are an expert blog content writer.
            Generate a creative and SEO-friendly blog title about: {state["topic"]}

            Return only the title.
            """

            messages = [
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)

            return {
                "blog": {
                    "title": response.content.strip()
                }
            }

    # ---------------------------------------------------------
    # CONTENT GENERATION
    # ---------------------------------------------------------
    def content_generation(self, state: BlogState):
        """
        Generate full blog content
        """

        if "topic" in state and state["topic"]:

            prompt = f"""
            You are an expert blog writer.
            Write a detailed blog post about: {state["topic"]}

            - Use Markdown formatting
            - Include headings and subheadings
            - Keep it well structured
            """

            messages = [
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)

            return {
                "blog": {
                    "title": state["blog"]["title"],
                    "content": response.content.strip()
                }
            }

    # ---------------------------------------------------------
    # TRANSLATION
    # ---------------------------------------------------------
    def translation(self, state: BlogState):
        """
        Translate the blog content to the specified language.
        """

        blog_content = state["blog"]["content"]
        blog_title = state["blog"]["title"]

        prompt = f"""
        You are a professional blog translator.

        Translate the following blog into {state["current_language"]}.
        - Maintain the original tone.
        - Maintain Markdown formatting.
        - Do NOT add extra commentary.
        - Return only the translated blog content.

        ORIGINAL CONTENT:
        {blog_content}
        """

        messages = [
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)

        return {
            "blog": {
                "title": blog_title,
                "content": response.content.strip()
            }
        }

    # ---------------------------------------------------------
    # ROUTING HELPERS
    # ---------------------------------------------------------
    def route(self, state: BlogState):
        return {"current_language": state["current_language"]}

    def route_decision(self, state: BlogState):
        """
        Route to appropriate translation node
        """

        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state["current_language"]
