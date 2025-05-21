function playPokemonCry(url) {
    const audio = new Audio(url);
    audio.play().catch(error => {
        console.error("Erreur lors de la lecture du son:", error);
        alert("Impossible de jouer le cri du Pokémon");
    });
} 