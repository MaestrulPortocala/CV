package Proiect2.Clase;

import javax.swing.*;
import java.awt.*;

public class Alt_Menu extends Menu {
    static public JPanel colorare(Image poza, Image scaledFigure1, Image scaledFigure2){
        Elemente.x1=300;
        Elemente.x2=600;
        Elemente.y1=400;
        Elemente.y2=400;
        JPanel backgroundPanel = new JPanel() {
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                ImageIcon backGround = new ImageIcon(poza);
                g.drawImage(backGround.getImage(), 0, 0, getWidth(), getHeight(), this);
                g.drawImage(scaledFigure1, Elemente.x1, Elemente.y1, 425, 300, this);
                g.drawImage(scaledFigure2, Elemente.x2, Elemente.y2, 300, 300, this);
            }
        };
        return backgroundPanel;
    }

}
