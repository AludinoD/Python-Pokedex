# Semester 1 Assessment 2 - Data Driven Application
# Pokedex Application (Using Pokemon API)
# Pokemon API: https://pokeapi.co
# Theme: Pokedex from the Kanto Region(GUI)
# By: Deniz Marc Andrei Aludino
# This Pokedex application was made from Figma(GUI), copying the design of a Pokedex from the Kanto Region.
# Also the main Functions of this app are also inspired from the Pokedex in the Games/Shows.
# It's a digital encyclopedia that catalogues and provides data on every Pokémon species encountered by a trainer.
# And it's mainly used to use it to log information like types, abilities, habitats, and evolutions, essentially "catching 'em all" to complete its database.
# Now this Pokedex doesn't completely have all the features of a real Pokedex.
# But it does have the main features such as searching for the Pokemon by name or ID, seeing their stats, nature types, and Evolutions.

# Libraries 
import requests # For Fetching Data from the API
import tkinter as tk # Tkinter GUI
import random # Random Pokemon
from PIL import Image, ImageTk # For Image Handling
from io import BytesIO # For storing image data in memory
from tkinter import messagebox # For message boxes
import pygame # Sound Effects

# Color Variables
redBg = "#E0082F" # Same Color as the Pokedex Background to blend elements
whiteBg = "#ffffff" # Simple White Color for Panels


# Pokedex Panel Flow
# Search Entry -> Search Button -> Fetch Pokemon Data -> Display Pokemon Data in the Pokedex UI(Image, Name, ID, Types, Stats)
# Next Button -> Load Next Pokemon by ID -> Update UI
# Previous Button -> Load Previous Pokemon by ID -> Update UI
# Random Button -> Load Random Number From 1 to 898 -> Get Data from the ID Number -> Update UI
# Favorite Button -> Add Current Pokemon ID to Favorites Set -> Show Messagebox Confirmation
# Favorites Tab Button -> Open Favorites Window -> Display all Favorite Pokemons in a Grid -> Click to Open In Main Pokedex -> Click Remove to remove from Favorites
# Compare Tab Button -> Open Compare Window -> Input 2 Pokemon Names/IDs -> Get Data for both Pokemons -> Display Side by Side, just like how its done in the main screen.
# Evolution Button -> Open Evolution Window -> Fetch Evolution Chain from the API -> Display the Chain -> Click to Open Pokemon in Main Pokedex




# Color Variables for Stats and Pokemon Types
statColors = {
    "hp": "#4CAF50",
    "attack": "#F44336",
    "defense": "#2196F3",
    "special-attack": "#FF9800",
    "special-defense": "#9C27B0",
    "speed": "#00BCD4"
}

# Pokemon Nature Type colors
typeColors = {
    "normal":"#A8A77A","fire":"#EE8130","water":"#6390F0",
    "electric":"#F7D02C","grass":"#7AC74C","ice":"#96D9D6",
    "fighting":"#C22E28","poison":"#A33EA1","ground":"#E2BF65",
    "flying":"#A98FF3","psychic":"#F95587","bug":"#A6B91A",
    "rock":"#B6A136","ghost":"#735797","dragon":"#6F35FC",
    "dark":"#705746","steel":"#B7B7CE","fairy":"#D685AD"
}

# Stats Order
statOrder = [
    "hp", "defense", "speed",
    "attack", "special-attack", "special-defense"
]

# API URLS
baseURL = "https://pokeapi.co/api/v2/pokemon/"
speciesURL = "https://pokeapi.co/api/v2/pokemon-species/"

# Load Images
# Background Image
bgImage = Image.open("PokeDex.png")
bgImage = bgImage.resize((600,700))

# Compare Background Image
compareImg = Image.open("Compare.png")
compareImg = compareImg.resize((600,700))


# Sound Effects
pygame.mixer.init()
pygame.mixer.music.load("BgMusic.mp3")
pygame.mixer.music.play(-1)  # Play background music on loop
bgmVol = 0.3 # Initialize Volume
pygame.mixer.music.set_volume(bgmVol) # Set Volume


#---------------------------------Pokedex Class-----------------------------------
class Pokedex(tk.Tk):
    # Initializing Pokemon Application
    def __init__(self):
        super().__init__()
        # Pokedex Window Configurations
        self.geometry("600x700")
        self.title("Kanto's PokeDéx")
        self.resizable(False,False)
        self.configure(bg=redBg)
        self.iconbitmap("Pokeball.ico")
        self.favorites = set()

        # Set Pokemon ID
        self.currentID = 1
        self.tkImg = None
        # Initialize False Shiny State
        self.isShiny = False
        
        # Build Pokedex UI and Load the first Pokemon
        self.BuildUI()
        self.loadPokemon(1)



#---------------------------------Button Styles-----------------------------------
    # Yellow Buttons
    def coloredButton(self,parent, text, command= None, width=10, fontSize=10):

        btn = tk.Button(parent,text=text,font=("Arial", fontSize, "bold"),width=width,command=command,
            bg="#E5FF00",fg="#000000",
            activebackground="#FFDD00",activeforeground="black",
            cursor="hand2",highlightbackground="black",highlightthickness=1
        )

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#D1C000"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#E5FF00"))

        return btn

    # White Buttons
    def styledButton(self,parent, text, command= None, width=10, fontSize=10):

        btn = tk.Button(parent,text=text,font=("Arial", fontSize, "bold"),width=width,command=command,
            bg="#FFFFFF",fg="#000000",
            activebackground="#E21E00",activeforeground="white",
            cursor="hand2",highlightbackground="black",highlightthickness=1
        )

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#C1C1C1"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#FFFFFF"))

        return btn

#---------------------------------Pokedex Functions-----------------------------------



    # Function to get Pokemon data for Favorites tab
    def getPokemonData(self, pokeID):
        # Fetch Pokemon Data from the API
        data = self.fetch(baseURL + str(pokeID))
        # Error Handling for Invalid Pokemon
        if not data:
            return {"name": f"Unknown #{pokeID}", "image": None}
        
        # Get Name
        name = data["name"].title()
        
        # Get Image and check if its shiny or not
        if self.isShiny:
            imgURL = data["sprites"]["other"]["official-artwork"]["front_shiny"]
        else:
            imgURL = data["sprites"]["other"]["official-artwork"]["front_default"]
        if imgURL:
            imgData = requests.get(imgURL).content
            img = Image.open(BytesIO(imgData)).resize((100, 100))
        else:
            # Fallback blank image
            img = Image.new("RGBA", (100, 100), (255, 255, 255, 0))
        # Return Name and Image Data
        return {"name": name, "image": img}

#---------------------------------Pokedex GUI-----------------------------------
    # Function for creating the Pokedex UI
    def BuildUI(self):
        # Set Background Image
        self.bgImgTk = ImageTk.PhotoImage(bgImage)
        self.bgLabel = tk.Label(self, image=self.bgImgTk)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Above Box Panel

        # Search Bar
        # Placeholder Text
        placeholder = "Put Pokémon name or ID"

        # Search Entry Box
        self.search_entry = tk.Entry(self, width=30, fg="grey")
        self.search_entry.place(x=105, y=100)
        # Search Entry Text Placeholder
        self.search_entry.insert(0, placeholder)

        # Functions for Search Entry
        # Focus In - Clears Placeholder when Focused In
        def onFocusIn(event):
            if self.search_entry.get() == placeholder:
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg="black")
            self.search_entry.after(1, lambda: self.search_entry.select_range(0, tk.END))

        # Focus Out - Restores Placeholder text if empty
        def onFocusOut(event):
            if self.search_entry.get() == "":
                self.search_entry.insert(0, placeholder)
                self.search_entry.config(fg="grey")

        # Clears the Entry after pressing Enter
        def onEnter(event): 
            self.search() 
            # Clear after pressing Enter 
            self.search_entry.delete(0, tk.END) 
            # Add Placeholder Back
            self.search_entry.insert(0, placeholder) 
            self.search_entry.config(fg="black") 
            # Re‑highlight placeholder for convenience 
            self.search_entry.after(1, lambda: self.search_entry.select_range(0, tk.END))

        
        # Bindings
        self.search_entry.bind("<FocusIn>", onFocusIn)
        self.search_entry.bind("<FocusOut>", onFocusOut)
        self.search_entry.bind("<Return>", onEnter)

        # Set Focus to Search Entry on Startup
        self.search_entry.focus_set()
        self.search_entry.after(1, lambda: self.search_entry.select_range(0, tk.END))

        # Search Buttons
        self.styledButton(self, text="Search",width=10,command=self.search).place(x=310,y=97)
        self.styledButton(self, text="Random",width=10,command=self.randomPokemon).place(x=410,y=97)

        # Miscs
        self.styledButton(self, text="Favorites", width=10, command=self.openFavorites).place(x=310,y=45)
        self.styledButton(self, text="Compare Pokemon",width=15,command=self.openCompare).place(x=410,y=45)
        self.favoriteBtn = self.coloredButton(self, text="⭐Favorite",width=10,command=self.toggleFavorite)
        self.favoriteBtn.place(x=403,y=130)

        # Shiny Button
        self.shinyBtn = self.coloredButton(self, text="✨Shiny",width=10,command=self.toggleShiny)
        self.shinyBtn.place(x=105, y=130)

        # Inside Box Panel

        # Navigation Buttons
        self.styledButton(self, text="Previous",width=10,command=self.prevPokemon).place(x=200,y=310)
        self.styledButton(self, text="Next",width=10,command=self.nextPokemon).place(x=300,y=310)
        
        

        # Pokemon Image
        self.pokemonImgLabel = tk.Label(self,bg=whiteBg,anchor="center")
        self.pokemonImgLabel.place(x=220,y=170)

        # Pokemon Name and ID
        self.pokemonNameLabel = tk.Label(self,bg=whiteBg,font=("Arial",12,"bold"),anchor="center")
        self.pokemonNameLabel.place(x=260,y=150)

        self.pokemonIDLabel = tk.Label(self,bg=whiteBg,font=("Arial",10,"bold"))
        self.pokemonIDLabel.place(x=280,y=130)


        # Stats Panel
        self.statsPanel = tk.Frame(self,bg=whiteBg,width=395,height=260,highlightbackground="black",highlightthickness=1)
        self.statsPanel.place(x=100,y=400)

        # Stats Labels
        self.statsLabel = tk.Label(self.statsPanel,text="Stats:",bg=whiteBg).place(x=5,y=5)
        self.typeLabels = []
        # Creates type labels for their respective type
        for i in range(2):
            # Initialize The Label
            lbl = tk.Label(self.statsPanel, fg="white", width=10, font=("Arial", 9, "bold"))
            # Place the label
            lbl.place(x=140 + i * 90, y=7)
            # Add to the list for update
            self.typeLabels.append(lbl)

        # Store Stat Bars and Values
        self.statBars = {}
        self.statValues = {}

        # Stat Bars and Values
        y = 40
        for stat in statOrder:
            # Stat Name Label
            tk.Label(self.statsPanel, text=stat.replace("-", " ").title(), bg=whiteBg).place(x=20, y=y)

            # Background Bar of the Stats
            bgBar = tk.Frame(self.statsPanel, bg="#ccc", width=200, height=14,highlightbackground="black",highlightthickness=1)
            bgBar.place(x=140, y=y+3)

            # Main Bar of the Stats
            bar = tk.Frame(self.statsPanel, bg=statColors[stat], height=14,highlightbackground="black",highlightthickness=1)
            bar.place(x=140, y=y+3)

            # Stat Value Number Label
            valuelbl = tk.Label(self.statsPanel, bg=whiteBg, font=("Arial", 9, "bold"))
            valuelbl.place(x=360, y=y)

            # Store References to update Bars and Values
            self.statBars[stat] = bar
            self.statValues[stat] = valuelbl
            y += 30

        # Evolution Button
        self.styledButton(self.statsPanel,text="See Pokemon Evolution",width=25,command=self.openEvolution).place(x=100, y=225)  

#---------------------------------Favorites Function-----------------------------------

    def toggleFavorite(self):
        if self.currentID in self.favorites:
            self.favorites.remove(self.currentID)
            messagebox.showinfo("Favorites",f"{self.pokemonNameLabel.cget('text')} Removed from favorites!")  
        else:
            self.favorites.add(self.currentID)
            messagebox.showinfo("Favorites",f"{self.pokemonNameLabel.cget('text')} added to favorites!")  

        self.updateFavoriteButton()
        

        if hasattr(self, "favoritesWindow") and self.favoritesWindow.winfo_exists():
            self.favoritesWindow.loadFavorites()

    def updateFavoriteButton(self):
        if self.currentID in self.favorites:
            self.favoriteBtn.config(text="Favorited")
        else:
            self.favoriteBtn.config(text="⭐Favorite")


#---------------------------------API-----------------------------------


    # Fetch Data from the Pokemon API
    def fetch(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
            return None
        except:
            return None

    # Load Pokemon Data into the Pokedex
    def loadPokemon(self,identifier):
        data = self.fetch(baseURL + str(identifier).casefold())
        # Error Handling for Invalid Pokemon
        if not data:
            messagebox.showerror("Error", "Pokémon not Found! Please check the name or ID and try again.")
            return

        # Get Pokemon Data and Update the UI
        # Gets the Pokemon ID, Name, and Image
        self.currentID = data["id"]
        self.pokemonIDLabel.config(text=f"#{data['id']:03}")
        self.pokemonNameLabel.config(text=data["name"].title())


        # Get Image and check if its shiny or not                           
        if self.isShiny:
            imgURL = data["sprites"]["other"]["official-artwork"]["front_shiny"]
        else:
            imgURL = data["sprites"]["other"]["official-artwork"]["front_default"]

        # Request Image Data
        imgData = requests.get(imgURL).content
        # Resize
        img = Image.open(BytesIO(imgData)).resize((130,130))
        # Display Pokemon Image that was fetched.
        self.tkImg = ImageTk.PhotoImage(img)
        self.pokemonImgLabel.config(image=self.tkImg)



        # Pokemon Types
        for lbl in self.typeLabels:
            lbl.config(text="", bg=whiteBg)

        # Set the type label of the Pokemon, Basing from the data fetched of the nature type
        for i, t in enumerate(data["types"]):
            name = t["type"]["name"]
            self.typeLabels[i].config(text=name.title(),bg=typeColors.get(name, "black"),highlightbackground="black",highlightthickness=1)

        # Stats
        for s in data["stats"]:
            # Store Stat name and Value
            stat = s["stat"]["name"]
            # Store values
            val = s["base_stat"]
            # Update Stat Bars and Values
            if stat in self.statBars:
                # Calculate the width of the bar based on the max stat value of 255
                width = min(250, int((val / 255) * 250))
                # Update the width and Value
                self.statBars[stat].config(width=width)
                self.statValues[stat].config(text=str(val))

#---------------------------------Functions-----------------------------------

    # Next Pokemon
    def nextPokemon(self):
        # Add 1 to the Current ID
        self.loadPokemon(self.currentID + 1)

    # Previous Pokemon
    def prevPokemon(self):
        if self.currentID > 1:
            # Subtracts 1 From the current Id if its greater than 1
            self.loadPokemon(self.currentID - 1)

    # Random Pokemon
    def randomPokemon(self):
        # Choose from 1 to 1025(Current Max pokemon)
        self.loadPokemon(random.randint(1, 1025))

    # Search bar Function
    def search(self):
        # Store Query from the Entry Box
        q = self.search_entry.get().strip().casefold()
        if q:
            self.loadPokemon(q)


    # Function to Open Compare Window
    def openCompare(self):
        CompareWindow(self)

    # Open Favorites Window
    def openFavorites(self):
        if hasattr(self, "favoritesWindow") and self.favoritesWindow.winfo_exists():
            self.favoritesWindow.lift()
        else:
            self.favoritesWindow = FavoritesWindow(self) 

    # Toggle Shiny Function
    def toggleShiny(self):
        # Toggle the state
        self.isShiny = not self.isShiny

        # Update button text after clicking
        if self.isShiny:
            self.shinyBtn.config(text="Unshiny")
        else:
            self.shinyBtn.config(text="✨Shiny")

        # Reload current Pokémon with new shiny state
        self.loadPokemon(self.currentID)

    # Function for Opening the Evo Window
    def openEvolution(self):
        evoWindow(self,self.currentID)

#---------------------------------Evolution Window-----------------------------------
class evoWindow(tk.Toplevel):
    # Initialize Evolution Window
    def __init__(self,parentApp, pokeID):
        super().__init__()

        # Store the parent App Reference
        self.parentApp = parentApp
        # Window Configurations
        self.title("Evolution Chain")
        self.geometry("600x250")
        self.configure(bg=redBg)
        self.iconbitmap("Pokeball.ico")

        # Title
        tk.Label(self, text="Evolution Chain", bg=redBg, font=("Arial", 14, "bold"),fg="white").pack(pady=10)

        # Centering the Frame
        self.centerFrame = tk.Frame(self, bg=redBg)
        self.centerFrame.pack(expand=True)
        # Frame for the Pokemon Chain
        self.chainFrame = tk.Frame(self.centerFrame, bg=redBg, height=170)
        self.chainFrame.pack(pady=10, fill="x")

        # Store Images 
        self.images = []
        # Load Evolution Chain
        self.loadChain(pokeID)
    

    # Function for loading the evolution chain
    def loadChain(self, pokeID):
        # Get Evolution Data from the API
        species = requests.get(speciesURL + str(pokeID)).json()
        # Get the Evo Chain URL
        evoURL = species["evolution_chain"]["url"]
        # Get the Evo Chain Data
        chain = requests.get(evoURL).json()["chain"]

        # Stores Data of the Evo List
        evoList = []

        # Traverse the Evolution Chain, by the species, name, and what it evolves to after
        def traverse(node):
            evoList.append(node["species"]["name"])
            for e in node["evolves_to"]:
                traverse(e)

        # Display Data and the Chain
        traverse(chain)
        
        # Create the Evolution Cards(Frame) from the evolist
        for i, name in enumerate(evoList):
                self.createEvolutionCard(name)

                # Add arrow for the next evolution,except after last evolution
                if i < len(evoList) - 1:
                    tk.Label(self.chainFrame,text="→",font=("Arial", 24, "bold"),bg=redBg).pack(side="left", padx=10)



    # Function for creating the Evolution Card
    # Picture, ID, and Name in a stack
    def createEvolutionCard(self, name):
        pokeData = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{name}").json()
        
        # Get Pokemon ID
        pokeID = pokeData["id"]

        # Get Pokemon Image and Display it.
        imgURL = pokeData["sprites"]["other"]["official-artwork"]["front_default"]
        # Request Image Data
        imgData = requests.get(imgURL).content
        # Resize Image
        img = Image.open(BytesIO(imgData)).resize((96, 96))
        # Set Image
        tkImg = ImageTk.PhotoImage(img)
        # Keep Reference
        self.images.append(tkImg)

        # Card Frame 
        card = tk.Frame(self.chainFrame, bg=whiteBg, width=160, height=160,highlightbackground="black",highlightthickness=1,cursor="hand2")
        card.pack(side="left", padx=10)
    
        # Card Content Labels and Format
        tk.Label(card, image=tkImg, bg=whiteBg).pack()
        tk.Label(card, text=f"#{pokeID:03}", bg=whiteBg, font=("Arial", 9, "bold")).pack()
        tk.Label(card, text=name.title(), bg=whiteBg, font=("Arial", 10)).pack()

        # Make the card clickable, making them open in the main Pokedex
        for widget in card.winfo_children():
            # Bind the click event with button 1
            widget.bind("<Button-1>", lambda e, pid=pokeID: self.openPokemon(pid))
        # Also Bind the card with the click Event
        card.bind("<Button-1>", lambda e, pid=pokeID: self.openPokemon(pid))

    # Function to open the selected Pokemon, and closing the evo window
    def openPokemon(self, pokeID):
        self.parentApp.loadPokemon(pokeID)
        self.destroy()

#---------------------------------Favorites Window-----------------------------------

# Favorite Window Class
class FavoritesWindow(tk.Toplevel):
    def __init__(self, parentApp):
        super().__init__()
        self.parentApp = parentApp
        # Window Configuration
        self.title("Favorite Pokémon")
        self.geometry("600x500")
        self.configure(bg=redBg)
        self.iconbitmap("Pokeball.ico")
        self.resizable(False, False)

        # Title
        tk.Label(self,text="⭐ Favorites",bg=redBg,fg="white",font=("Arial", 16, "bold")).pack(pady=10)

        # Center frame
        self.centerFrame = tk.Frame(self, bg=redBg)
        self.centerFrame.pack(expand=True, fill="both")

        # Scrollable canvas
        self.canvas = tk.Canvas(self.centerFrame, bg=redBg, highlightthickness=0)
        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.centerFrame, orient="vertical", command=self.canvas.yview)
        # Bind scrollbar to canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Position Canvas and Scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame to hold the grid
        self.cardsFrame = tk.Frame(self.canvas, bg=redBg)
        self.cardsWindow = self.canvas.create_window((0, 0), window=self.cardsFrame, anchor="n")

        # Scroll region and centering
        def updateScrollRegion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Bind the event and update scroll region
        self.cardsFrame.bind("<Configure>", updateScrollRegion)

        # Center the cardsFrame in the Canvas
        def centerCardsFrame(event):
            canvasWidth = event.width
            # Get width of the frame
            cardsWidth = self.cardsFrame.winfo_reqwidth()
            # Calculate x offset to center
            xOffset = max((canvasWidth - cardsWidth) // 2, 0)
            # Set position
            self.canvas.coords(self.cardsWindow, xOffset, 0)

        self.canvas.bind("<Configure>", centerCardsFrame)

        # Make scrollable using Mouse Wheel
        def onMouseWheel(event):
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # Bind MouseWheel
        self.canvas.bind_all("<MouseWheel>", onMouseWheel)

        # Keep image references
        self.images = []

        # Load favorites
        self.loadFavorites()
    
    # Function to load Favorite Pokemons in the Tab
    def loadFavorites(self):
        # Max of 3 Columns
        maxCols = 3
        # Sorts Favorite List by ID
        favorites = sorted(self.parentApp.favorites)

        # Clear previous content
        for widget in self.cardsFrame.winfo_children():
            widget.destroy()
        self.images.clear()

        # If there are no favorites set yet
        if not self.parentApp.favorites:
            tk.Label(self.cardsFrame, text="No favorites yet",bg=redBg, fg="white").pack(pady=20)
            return

        # Create Cards for each favorite Pokemon
        for idx, pokeID in enumerate(favorites):
            # calculate the row and Column for each card in the grid
            row = idx // maxCols
            col = idx % maxCols

            # Get Pokemon Data based from the ID
            pokemon = self.parentApp.getPokemonData(pokeID)

            # Card frame
            card = tk.Frame(self.cardsFrame, bg=whiteBg, width=160, height=220, bd=2, relief="raised",cursor="hand2")
            card.grid_propagate(False)
            card.grid(row=row, column=col, padx=10, pady=10)

            # Pokémon Image
            img = pokemon['image']
            tkImg = ImageTk.PhotoImage(img)
            self.images.append(tkImg)
            labelImg = tk.Label(card, image=tkImg, bg=whiteBg)
            labelImg.pack(pady=5)

            # Name & ID
            tk.Label(card, text=pokemon['name'], bg=whiteBg, font=("Arial", 12, "bold")).pack()
            tk.Label(card, text=f"#{pokeID:03}", bg=whiteBg, font=("Arial", 10)).pack(pady=5)

            # Check if favorited
            if pokeID in self.parentApp.favorites:
                btnTxt = "Favorited"
            else:
                btnTxt = "Remove"

            # Remove Favorite Button
            removeBtn = self.styledButton(card, text=btnTxt, bg=redBg, fg="white", fontSize=10,command=lambda pid=pokeID: self.removeFavorite(pid))
            removeBtn.pack(pady=5)

            # Hover effect for favorited text
            def onEnter(e, btn=removeBtn, pid=pokeID):
                if pid in self.parentApp.favorites:
                    btn.config(text="Remove")

            def onLeave(e, btn=removeBtn, pid=pokeID):
                if pid in self.parentApp.favorites:
                    btn.config(text="Favorited")

            removeBtn.bind("<Enter>", onEnter)
            removeBtn.bind("<Leave>", onLeave)


            # Clickable card/image
            card.bind("<Button-1>", lambda e, pid=pokeID: self.selectPokemon(pid))
            labelImg.bind("<Button-1>", lambda e, pid=pokeID: self.selectPokemon(pid))

        # Center the last row if incomplete
        total_rows = (len(favorites) + maxCols - 1) // maxCols
        for r in range(total_rows):
            self.cardsFrame.grid_rowconfigure(r, weight=1)
        for c in range(maxCols):
            self.cardsFrame.grid_columnconfigure(c, weight=1)

    # Function to Remove Pokemon
    def removeFavorite(self, pid):
        self.parentApp.favorites.remove(pid)
        self.parentApp.updateFavoriteButton()
        self.loadFavorites()

    # Function to Select Pokemon and Open it in the main Pokedex, closing the tab
    def selectPokemon(self, pokeID):
        self.parentApp.loadPokemon(pokeID)
        self.destroy()

    # Styled Button Here aswell
    def styledButton(self, parent, text, command=None, width=10, fontSize=10, bg="#AE0000", fg="#000000"):
        btn = tk.Button(parent,text=text,font=("Arial", fontSize, "bold"),width=width,command=command,bg=bg,fg=fg,
                        activebackground="#E21E00",activeforeground="white",cursor="hand2",
                        highlightbackground="black",highlightthickness=1)

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#B50000"))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

#---------------------------------Compare Window-----------------------------------

# This Area is the same as the main Pokedex, but it displays 2 Pokemons Side by Side for comparison
# Compare Window Class
class CompareWindow(tk.Toplevel):
    def __init__(self, parentApp):
        super().__init__()
        self.parentApp = parentApp
         
        # Window Configurations
        self.title("Compare Pokémon")
        self.geometry("600x700")
        self.configure(bg=redBg)
        self.iconbitmap("Pokeball.ico")
        self.resizable(False, False)

        # Background Image
        self.compareImgTk = ImageTk.PhotoImage(compareImg)
        self.compareLabel = tk.Label(self, image=self.compareImgTk)
        self.compareLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        tk.Label(self,text="Compare Pokémon",bg=redBg,fg="white",font=("Arial", 16, "bold")).place(x=300,y=120,anchor="center")

        # Text Placeholders
        placeholder1 = "Pokémon 1 name/ID"
        placeholder2 = "Pokémon 2 name/ID"
        # Entry Boxes
        self.entry1 = tk.Entry(self, width=20, fg="grey", justify="center")
        self.entry2 = tk.Entry(self, width=20, fg="grey", justify="center")
        # Insert Placeholder texts
        self.entry1.insert(0, placeholder1)
        self.entry2.insert(0, placeholder2)
        # Place Entry Boxes
        self.entry1.place(x=80,y=150)
        self.entry2.place(x=380,y=150)

        # Entry Placeholder Functions
        # Box 1
        def onFocusIn1(event):
            if self.entry1.get() == placeholder1:
                self.entry1.delete(0, tk.END)
                self.entry1.config(fg="black")
        def onFocusOut1(event):
            if self.entry1.get().strip() == "":
                self.entry1.insert(0, placeholder1)
                self.entry1.config(fg="grey")
        # Box 2
        def onFocusIn2(event):
            if self.entry2.get() == placeholder2:
                self.entry2.delete(0, tk.END)
                self.entry2.config(fg="black")
        def onFocusOut2(event):
            if self.entry2.get().strip() == "":
                self.entry2.insert(0, placeholder2)
                self.entry2.config(fg="grey")

        # Bindings
        self.entry1.bind("<FocusIn>", onFocusIn1)
        self.entry1.bind("<FocusOut>", onFocusOut1)
        self.entry2.bind("<FocusIn>", onFocusIn2)
        self.entry2.bind("<FocusOut>", onFocusOut2)


        # Compare Button
        self.styledButton(self, text="Compare", command=self.compare, fontSize=10, width=10).place(x=300, y=160, anchor="center")

        # Pokemon Frames
        self.poke1Frame = tk.Frame(self, bg=redBg)
        self.poke1Frame.grid(row=5, column=0, sticky="n", pady=10)
        self.poke2Frame = tk.Frame(self, bg=redBg)
        self.poke2Frame.grid(row=5, column=2, sticky="n", pady=10)

        # Grid Configuration
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Store Image 
        self.images = []
        
    # Function for Comparing the Pokemons
    def compare(self):
        # Clear previous Pokemon displays of Pokemon 1 and 2 frames
        for widget in self.poke1Frame.winfo_children():
            widget.destroy()
        for widget in self.poke2Frame.winfo_children():
            widget.destroy()
        self.images.clear()

        # Get Name or ID from the Boxes
        p1Name = self.entry1.get().strip()
        p2Name = self.entry2.get().strip()

        # Input Validation for Empty Boxes
        if p1Name.casefold() in ["", "pokémon 1 name/id"]:
            messagebox.showerror("Error", "Please enter Pokémon 1")
            return
        if p2Name.casefold() in ["", "pokémon 2 name/id"]:
            messagebox.showerror("Error", "Please enter Pokémon 2")
            return

        # Fetch Pokémon
        p1 = self.fetch(p1Name)
        p2 = self.fetch(p2Name)

        # Input Validation For Invalid Pokemons, Either one or Both
        if not p1 and not p2:
            messagebox.showerror("Error", "Both Pokémon not found!")
            return
        elif not p1:
            messagebox.showerror("Error", "Pokémon 1 not found!")
            return
        elif not p2:
            messagebox.showerror("Error", "Pokémon 2 not found!")
            return

        # Display Pokémon
        self.showPokemon(p1, self.poke1Frame)
        self.showPokemon(p2, self.poke2Frame)

        # Clear entries after successful compare
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)

    # Function to fetch Pokemon Data
    def fetch(self, q):
        try:
            r = requests.get(baseURL + str(q).casefold())
            return r.json() if r.status_code == 200 else None
        except:
            return None
    
    # Function to display the Pokemons in the Compare WIndow
    def showPokemon(self, data, parentFrame):
        frame = tk.Frame(parentFrame, bg=whiteBg, width=280, height=380, bd=2, relief="raised")
        frame.grid_propagate(False)
        frame.pack(pady=5)

        # Image Validation(If the image can't be fetched or Found)
        try:
            # Get Image
            imgURL = data["sprites"]["other"]["official-artwork"]["front_default"]

            if imgURL:
                imgData = requests.get(imgURL).content
                img = Image.open(BytesIO(imgData)).resize((120, 120))
                tkImg = ImageTk.PhotoImage(img)
                self.images.append(tkImg)
                tk.Label(frame, image=tkImg, bg=whiteBg).pack(pady=5)
            else:
                tk.Label(frame, text="No Image", bg=whiteBg).pack(pady=5)
        except:
            tk.Label(frame, text="No Image", bg=whiteBg).pack(pady=5)

        # Name and ID
        tk.Label(frame, text=data["name"].title(), font=("Arial", 12, "bold"), bg=whiteBg).pack()
        tk.Label(frame, text=f"#{data['id']:03}", font=("Arial", 10), bg=whiteBg).pack(pady=2)

        # Pokemon Types
        typeFrame = tk.Frame(frame, bg=whiteBg)
        typeFrame.pack(pady=5)
        for t in data["types"]:
            typeName = t["type"]["name"]
            tk.Label(typeFrame, text=typeName.title(), bg=typeColors.get(typeName, "black"),
                     fg="white", font=("Arial", 9, "bold"), width=10,highlightbackground="black",highlightthickness=1).pack(side="left", padx=5)

        # Pokemon Stats
        statsFrame = tk.Frame(frame, bg=whiteBg)
        statsFrame.pack(pady=5)
        for stat in statOrder:
            statData = next((s for s in data["stats"] if s["stat"]["name"] == stat), None)
            if statData:
                val = statData["base_stat"]
                tk.Label(statsFrame, text=f"{stat.replace('-', ' ').title()}: {val}", font=("Arial", 9), bg=whiteBg).pack(anchor="w", padx=5)
                bar = tk.Frame(statsFrame, bg=statColors.get(stat, "gray"), width=int((val / 255) * 200), height=10,highlightbackground="black",highlightthickness=1)
                bar.pack(anchor="w", padx=5, pady=2)

    # Added Button Here aswell because styled button is outside of this class
    def styledButton(self, parent, text, command=None, width=10, fontSize=10, bg="#FFFFFF", fg="#000000"):
        btn = tk.Button(parent,text=text,font=("Arial", fontSize, "bold"),width=width,command=command,
            bg=bg,fg=fg,cursor="hand2",
            activebackground="#E21E00",activeforeground="white",
            highlightbackground="black",highlightthickness=1
        )

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#C1C1C1"))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

# Run the Application
if __name__ == "__main__":
    app = Pokedex()
    app.mainloop()
