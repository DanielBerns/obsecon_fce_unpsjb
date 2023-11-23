from components.webdeprecios.bot import update

if __name__ == "__main__":
    website = "https://www.obs-econ-fce.unp.edu.ar/"
    username = "observatorio"
    commands = ["Este es el primer mensaje del servicio de noticias.", 
                "Aquí mostraremos las últimas novedades de la Web de Precios", 
                "La presentación publica de este sitio será el jueves 23 de noviembre de 2023 a las 15:30hs."]
    update(website, username, commands)
