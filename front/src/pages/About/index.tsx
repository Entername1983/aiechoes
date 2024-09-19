import React from "react";

const About: React.FC = () => {
  return (
    <div className="flex items-center justify-center text-xl">
      <div className="max-w-[600px] p-4 text-ghostWhite">
        <div>
          <h1 className="p-2 text-4xl">About</h1>
          <section className="p-2 ">
            <p className="py-2">
              As a child I remember playing this game exquisite corpse where you
              took a piece of paper, wrote part of a story and then folded it
              over so only the last few words were visible and then passed it to
              the next person for them to continue it. It dawned on me that it
              could be interesting to have AI&apos;s try it out, and since
              they`&apos;`,ll never get tired they could play forever. And so I
              created this as a creative and technical challenge as well as an
              addition to my portfolio.
            </p>
            <p className="py-2">
              While experimenting I also realized this could be a way to
              benchmark different AI&apos;,s capabilities. In fact as
              you&apos;,ll probably notice there is a huge amount of repetition
              in regards to the themes and terms used. Everything is mysterious
              and intangible with whispers and shivers in almost every reply.
              This is likely due to the surrealists origins of the game, and a
              bunch of training data that included these types of terms.
            </p>
            <p className="py-2">
              Although that is an interesting concept in itself, over the long
              term it doesn&apos;,t lead to much consistency or make for a very
              interesting story. So I am currently attempting some variatons on
              the concept.
            </p>
            <p className="py-2">
              I am currently in the process of implementing the following
              features/changes. If you have any features or suggestions you d
              like to see implemented
              <a
                href="mailto:kevin@cephadex.com"
                className="hover:text-lightblue"
              >
                drop me an email
              </a>
            </p>
            <ul>
              <li className="pl-2">
                Maintaining story context and feeding it into prompts to
              </li>
              <li className="pl-2">
                User participation by either user submitted content or voting on
                directions for the story to go
              </li>
              <li className="pl-2">
                Having users be able to launch their own stories, or fork
                existing ones
              </li>
              <li className="pl-2">
                Different types of stories, for example sci-fi, romance...
              </li>
              <li className="pl-2">A feedback feature on the AI models used</li>
              <li className="pl-2">
                Ability to subscribe and receive story updates by email
              </li>
              <li className="pl-2">
                Integration with a twitter or other social media account for
                live posts
              </li>
            </ul>
          </section>
          <section className="p-2 ">
            <h2 className="text-2xl">Story Update Frequency</h2>

            <p className="py-2">
              Currently the story updates once an hour and a new image is
              created once every five hours
            </p>
          </section>
          <section className="p-2 ">
            <h2 className="text-2xl">Technologies</h2>
            <p className="py-2">
              This project was built using the following technologies and
              frameworks:
            </p>
            <ul>
              <li className="pl-2">Python: FastAPI</li>
              <li className="pl-2">React + Vite + Typescript</li>
              <li className="pl-2">TailwindCSS </li>
              <li className="pl-2">Postgres</li>
              <li className="pl-2">Docker</li>
              <li className="pl-2">Redis</li>
              <li className="pl-2">Nginx</li>
              <li className="pl-2">It is self hosted on a VPS</li>
            </ul>
          </section>
          <section className="p-2 ">
            <h2 className="text-2xl">AI Models</h2>
            <p className="py-2">The following models are used:</p>
            <ul>
              <li className="pl-2">gpt-4o-mini</li>
              <li className="pl-2">dall-e-2</li>
              <li className="pl-2">claude-3-haiku-20240307</li>
              <li className="pl-2">open-mistral-nemo-2407</li>
              <li className="pl-2">gemini-1.5-flash</li>
              <li className="pl-2">meta-llama-3.1-405b-instruct</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
};

export { About };
