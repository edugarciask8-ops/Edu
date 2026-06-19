import os
import random
import requests

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
INSTAGRAM_TOKEN = os.environ["INSTAGRAM_TOKEN"]
INSTAGRAM_ACCOUNT_ID = os.environ["INSTAGRAM_ACCOUNT_ID"]

TEMAS = [
    ("Zaha Hadid", "fluidez orgánica, formas curvas futuristas, espacios blancos"),
    ("Tadao Ando", "hormigón visto, luz natural dramática, minimalismo japonés"),
    ("Le Corbusier", "modulor, planta libre, ventanas horizontales, brutalismo elegante"),
    ("Mies van der Rohe", "menos es más, acero y vidrio, espacios diáfanos"),
    ("Frank Lloyd Wright", "arquitectura orgánica, integración con la naturaleza, piedra y madera"),
    ("Rem Koolhaas", "espacios programáticos, escala monumental, mezcla de materiales"),
    ("Jean Nouvel", "luz y reflexión, fachadas innovadoras, materialidad sofisticada"),
    ("Peter Zumthor", "atmósfera sensorial, madera y piedra, silencio arquitectónico"),
]

ESPACIOS = [
    "salón minimalista con grandes ventanales",
    "cocina de lujo con isla central",
    "dormitorio con vistas al exterior",
    "baño de spa con luz natural",
    "estudio de trabajo elegante",
    "terraza con jardín vertical",
    "entrada de doble altura",
    "biblioteca con estanterías del suelo al techo",
]

CAPTIONS = [
    "¿Cómo diseñaría {disenador} este espacio? 🏛️\n\nArquitectura que inspira. Cada línea tiene una razón de ser.\n\n#arquitectura #diseñodeinteriores #arcoptima #interiordesign #architecture",
    "El estilo de {disenador} aplicado a interiores modernos ✨\n\nForma, función y belleza en perfecta armonía.\n\n#arquitectura #interiores #arcoptima #diseño #interiordesign",
    "Imagina vivir en un espacio diseñado por {disenador} 🖤\n\nDonde cada detalle cuenta.\n\n#arcoptima #architecture #interiors #diseñodeinteriores #homedecor",
]

def generar_imagen(disenador, estilo, espacio):
    prompt = (
        f"Interior design inspired by {disenador}'s architectural style: {estilo}. "
        f"Space: {espacio}. "
        f"Photorealistic, high-end architectural photography, professional lighting, 4K quality."
    )
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": "dall-e-3", "prompt": prompt, "n": 1, "size": "1024x1024"},
    )
    response.raise_for_status()
    return response.json()["data"][0]["url"]

def publicar_en_instagram(image_url, caption):
    # Paso 1: crear contenedor
    r = requests.post(
        f"https://graph.instagram.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": INSTAGRAM_TOKEN,
        },
    )
    r.raise_for_status()
    container_id = r.json()["id"]
    print(f"Contenedor creado: {container_id}")

    # Paso 2: publicar
    r2 = requests.post(
        f"https://graph.instagram.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        data={"creation_id": container_id, "access_token": INSTAGRAM_TOKEN},
    )
    r2.raise_for_status()
    print(f"Post publicado: {r2.json()}")

def main():
    disenador, estilo = random.choice(TEMAS)
    espacio = random.choice(ESPACIOS)
    caption = random.choice(CAPTIONS).format(disenador=disenador)

    print(f"Generando imagen: {disenador} — {espacio}")
    image_url = generar_imagen(disenador, estilo, espacio)
    print(f"Imagen generada: {image_url}")

    publicar_en_instagram(image_url, caption)
    print("Publicado en Instagram correctamente.")

if __name__ == "__main__":
    main()
