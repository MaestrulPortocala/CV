package Proiect2.Clase;
import javazoom.jl.player.Player;
import java.io.FileInputStream;

public class Music {
    private javazoom.jl.player.Player player;
    public void playMusic() {
        stopMusic();
        if(Elemente.play) {
            Thread playThread = new Thread(() -> {

                while (true) {
                    try {
                        FileInputStream fileInputStream = new FileInputStream("MortalKombat-main/Proiect2/Poze/01. Techno Syndrome (Mortal Kombat).mp3");
                        player = new Player(fileInputStream);
                        player.play();
                        if(!Elemente.play){
                            stopMusic();
                            break;
                        }
                    } catch (Exception ex) {
                        ex.printStackTrace();
                        break;
                    }
                }

            });
            playThread.start();
        }
    }


    public void stopMusic() {
        try {
            if (player != null) {
                player.close();
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
