
from flask import Flask, render_template, request

import agent

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    answer = None
    question = ""
    source = None

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        if question:

            try:

                invoker = getattr(agent, "invoke", None) or getattr(agent, "run", None)
                if invoker is None:
                    raise AttributeError("Agent module has no callable 'invoke' or 'run'.")

                response = invoker(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": question
                            }
                        ]
                    }
                )

                print("\n=== AGENT RESPONSE ===")
                print(response)

                messages = response.get(
                    "messages",
                    []
                )

                if messages:

                    answer = messages[-1].get(
                        "content",
                        "No answer found."
                    )

                else:

                    answer = "No response received."

                source = response.get(
                    "source",
                    "GameLore Knowledge Base"
                )

            except Exception as e:

                print("\n=== ERROR ===")
                print(str(e))

                answer = f"Error: {str(e)}"
                source = "System"

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        source=source
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
