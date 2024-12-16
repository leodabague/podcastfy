import gradio as gr
from podcastfy.client import generate_podcast
from dotenv import load_dotenv

load_dotenv()

# Define a function to generate the podcast
def generate_podcast_ui(urls, tts_model, llm_model, output_language, creativity, is_local, transcript_only, longform, user_instructions, question_voice, answer_voice, podcast_name, podcast_tagline, ending_message, conversation_style, engagement_techniques):
    podcast_config = {
        'output_language': output_language,
        'podcast_name': podcast_name,
        'podcast_tagline': podcast_tagline,
        "conversation_style": conversation_style,
        "engagement_techniques": engagement_techniques,
        "ending_message": ending_message,
        "creativity": creativity,
        "user_instructions": user_instructions,
        'text_to_speech': {
            'default_tts_model': tts_model,
            tts_model: {
                'default_voices': {
                    'question': question_voice, 
                    'answer': answer_voice
                },
                'model': 'eleven_multilingual_v2'
            }
        }
    }

    try:
        result = generate_podcast(
            urls=urls.split(","),
            tts_model=tts_model,
            llm_model_name=llm_model,
            api_key_label=f"{tts_model.upper()}_API_KEY",
            conversation_config=podcast_config,
            is_local=is_local,
            transcript_only=transcript_only,
            longform=longform
        )
        
        # Se result for uma string, é o caminho do arquivo
        if isinstance(result, str):
            try:
                with open(result, "r", encoding='utf-8') as file:
                    transcript_preview = file.read(2000) + "\n...\n" + f"Transcrição gerada: {result}"
                return f"Transcrição gerada com sucesso!\n\nPreview:\n{transcript_preview}"
            except Exception as e:
                return f"Arquivo gerado em: {result}"
        
        # Se for um dicionário, mantém o comportamento anterior
        elif isinstance(result, dict):
            if transcript_only:
                try:
                    with open(result["transcript"], "r", encoding='utf-8') as file:
                        transcript_preview = file.read(2000) + "\n...\n" + f"Transcrição gerada: {result['transcript']}"
                    return transcript_preview
                except Exception as e:
                    return f"Erro ao ler transcrição: {str(e)}"
            else:
                transcript_path = result.get("transcript", "Caminho da transcrição não disponível")
                audio_path = result.get("audio", "Caminho do áudio não disponível")
                return f"Transcrição gerada: {transcript_path}\nÁudio gerado: {audio_path}"
        
        else:
            return f"Tipo de retorno não esperado: {type(result)}"
            
    except Exception as e:
        return f"Erro ao gerar o podcast: {str(e)}"

# Create the Gradio interface
with gr.Blocks() as interface:
    gr.Markdown("# Podcastfy - Interface Gráfica")
    gr.Markdown("Insira as URLs e configurações para gerar seu podcast.")

    # Bloco 1: Configuração técnica
    with gr.Group():
        gr.Markdown("### Configuração Técnica")
        with gr.Row():
            tts_model_input = gr.Radio(choices=["elevenlabs", "openai", "geminimulti"], label="Modelo de TTS", value="elevenlabs")
            llm_model_input = gr.Textbox(label="Modelo de LLM", value="gpt-4o-mini")
        with gr.Row():
            question_voice_input = gr.Textbox(label="ID/Nome da Voz para Perguntas", value="vibfi5nlk3hs8Mtvf9Oy")
            answer_voice_input = gr.Textbox(label="ID/Nome da Voz para Respostas", value="CstacWqMhJQlnfLPxRG4")
        with gr.Row():
            is_local_input = gr.Checkbox(label="Usar LLM local", value=False)
            transcript_only_input = gr.Checkbox(label="Somente transcrição", value=False)
            longform_input = gr.Checkbox(label="Formato Longo", value=False)

    # Bloco 2: Configuração do Podcast
    with gr.Group():
        gr.Markdown("### Configuração do Podcast")
        with gr.Row():
            podcast_name_input = gr.Textbox(label="Nome do Podcast", value="IA com Leo")
            podcast_tagline_input = gr.Textbox(label="Tagline do Podcast", value="Construindo conhecimento")
        with gr.Row():
            output_language_input = gr.Radio(choices=["Portuguese", "English", "French"], label="Idioma de Saída", value="Portuguese")
            creativity_input = gr.Slider(minimum=0, maximum=1, step=0.1, label="Criatividade", value=0.7)
        with gr.Row():
            conversation_style_input = gr.CheckboxGroup(
                choices=["formal", "analytical", "critical", "narrative", "suspenseful", "descriptive", "instructional", "step-by-step", "casual", "humorous", "engaging", "fast-paced", "enthusiastic", "adventurous"],
                label="Estilo de Conversação",
                value=["casual", "engaging"]
            )
            engagement_techniques_input = gr.CheckboxGroup(
                choices=["rhetorical questions", "socratic questioning", "historical references", "thought experiments", "cliffhangers", "vivid imagery", "audience prompts", "code examples", "real-world applications", "troubleshooting tips", "anecdotes", "analogies", "humor", "vocabulary explanations", "cultural context", "pronunciation tips"],
                label="Técnicas de Engajamento",
                value=["rhetorical questions", "analogies"]
            )

    # Bloco 3: Configuração do Conteúdo
    with gr.Group():
        gr.Markdown("### Configuração do Conteúdo")
        with gr.Row():
            urls_input = gr.Textbox(label="URLs (separadas por vírgula)")
        with gr.Row():
            user_instructions_input = gr.Textbox(label="Instruções do Usuário")
            ending_message_input = gr.Textbox(label="Mensagem Final", value="Obrigado por acompanhar e até a próxima")

    generate_button = gr.Button("Gerar Podcast")
    output_message = gr.Textbox(label="Mensagem de Saída")

    generate_button.click(
        fn=generate_podcast_ui,
        inputs=[urls_input, tts_model_input, llm_model_input, output_language_input, creativity_input, is_local_input, transcript_only_input, longform_input, user_instructions_input, question_voice_input, answer_voice_input, podcast_name_input, podcast_tagline_input, ending_message_input, conversation_style_input, engagement_techniques_input],
        outputs=[output_message]
    )

# Run the app
interface.launch(share=False)
