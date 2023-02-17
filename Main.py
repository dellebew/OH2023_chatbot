import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random as rand
import os
from PIL import Image
import re
# from model import GeneralModel

# checks if api key is valid


def valid_api_key(inp: str):
    try:
        st.session_state.pred.model_prediction(
            input="test", api_key=inp)
        return True
    except Exception as e:
        st.error("API Key check failed: " + str(e))
        return False

# updates api kei in session state


def update_api_key(inp: str):
    st.session_state.api_key = inp


def app():
    if st.session_state.api_key:
        col1, col2 = st.columns(2)

        @st.cache
        def process_prompt(inp):
            return st.session_state.pred.model_prediction(input=str(inp).strip(), api_key=st.session_state.api_key)

        with col1:

            ### SETUPS ###

            # Setting up the Title
            st.title("Give our poet a style and topic")

            # available options for poets and nouns
            region_list = ["Asia", "Europe"]

            nouns_list = [
                "Singapore University of Technology and Design (SUTD)", "university education", "engineering", "STEM", "design thinking", "Humanities", "Science", "Technologies", "COVID"]
            eng_poets_list = ["Shakespeare", "Seamus Heaney", "Edgar Allan Poe", "William Blake", "Robert Frost",
                              "Emily Dickinson", "Oscar Wilde", "George Bernard Shaw", "William Wordsworth", "Sylvia Plath"]

            chi_poets = ["Li He", "Confucius", "Mencius", "LaoTzu"]

            jap_poets = ["Matsuo Basho"]

            poetry_forms = ['free verse', 'sonnet', 'acrostic', 'limerick',
                            'ode', 'solliloquy', 'elegy', 'ballad', 'villanelle', 'Victorian', 'Edwardian', 'Georgian', 'Baroque', 'Surrealistic', 'Shakespearean']

            asia_genres = ["Chinese: Airs (风)", "Chinese: Ode (雅)", "Chinese: Hymn (颂)", "Haiku", "Japanese: Tanka",
                           "Malay: Syair", "Burmese: Yadu", "Korean: Sijo", "Indian or Sri Lankan: Kural"]

            # available options for poets and nouns
            region_list = ["Asia", "Europe"]

            ### End of Setups ###

            ### Start of Web APP ###

            # with st.sidebar:
            region_option = st.selectbox(
                "Select a region", region_list)

            #  selected region will release the available choices
            if region_option == "Asia":
                poet_option = st.radio("Available Genre", options=asia_genres)
            elif region_option == "Europe":
                poet_option = st.radio(
                    "Available Genre", options=poetry_forms)

            # choices available for nouns
            noun_option = st.multiselect("Available Nouns", nouns_list)
            noun_option

            # finalised decision
            if st.button("Confirm choices"):
                # string the list
                filtered = ""
                for noun in noun_option:
                    filtered += f"{noun}, "
                filtered = filtered.strip()
                if len(filtered) > 0:
                    if filtered[-1] == ",":
                        filtered = filtered[:-1]
                    # st.write(filtered) # debug

                # Write to textbox
                st.session_state.textbox = "Write a " + poet_option + " style"\
                    " poem about the benefits of " + filtered + " in English"

        with col2:
            st.title("Pen is poised and ready")

            # for initializing textbox
            answer = st.text_area(
                "Use the prompt tweaked on the left or input your own text in English",
                key="textbox",
                max_chars=150
            )

            # backend processes
            # submit button
            report_text = ""
            if st.button("Pen my poem!"):
                try:
                    with st.spinner(text="In progress"):
                        report_text = process_prompt(st.session_state.textbox)
                        pattern = re.compile(r"(?<!\n)\n(?!\n)")
                        report_text_final = pattern.sub('\n\n', report_text)
                        st.markdown(report_text_final)
                except Exception as e:
                    st.error("Error: " + str(e))
                    restart = st.button("Re-enter API Key",
                                        on_click=update_api_key(""))

            # Generate wordcloud and text
            st.set_option("deprecation.showPyplotGlobalUse", False)
            text = report_text
            if text:
                wdcloud = WordCloud(background_color="white").generate(text)
                plt.figure(figsize=(10, 5))
                plt.tight_layout(pad=0)
                plt.imshow(wdcloud)
                plt.axis("off")
                idx = str(rand.randint(0, 1000))
                conti = ['a', 'b', 'c', 'd', 'e', 'f']
                choosen = rand.choice(conti)
                # save text
                cloudtext = open(f"texts/wordcloud{idx}{choosen}.txt", 'w')
                cloudtext.write(text)
                cloudtext.close()
                # save images
                plt.savefig(
                    f"clouds/wordcloud{idx}{choosen}.png", bbox_inches='tight', dpi=300)
                plt.show()
                st.pyplot()

    else:
        with st.form("API_Key_Form"):
            api_key = st.text_input("APIkey", type="password")

            submitted = st.form_submit_button("Submit")
            if submitted:
                if valid_api_key(api_key):
                    update_api_key(api_key)
                    st.experimental_rerun()
        # st.error("🔑 Please enter API Key")
