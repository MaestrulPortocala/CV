package Proiect2.Program;

import Proiect2.Clase.*;
import Proiect2.Clase.Menu;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;


public class Kombat extends Sablon implements ActionListener {
    Image scaledWin1, scaledWin2;
    String text;
    JProgressBar healthBar1, healthBar2;
    Random chance = new Random();
    int health1 = Names.p1.getHealth();
    int health2 = Names.p2.getHealth();
    int turn=chance.nextInt(2);
    int option;
    int count=0, count1=0, count2=0, count3=0;
    boolean retras=false, atac=false, gata=false, sus=false, sus1=false;
    Timer timer=new Timer(30, this);
    Timer timer1=new Timer(30, _-> {
            int jump=1;
            if(count1<10 && !sus) {

                Elemente.y1 += jump;
                count1+=jump;
                repaint();
                if(count1>=10){
                    sus=true;
                }
            }
            if(count1>0 && sus) {
                Elemente.y1 -= jump;
                count1-=jump;
                repaint();
                if(count1<=0){
                    sus=false;
                }
            }
            if(count2<10 && !sus) {
                Elemente.y2 += jump;
                count2+=jump;
                repaint();
                if(count2>=10){
                    sus1=true;
                }
            }
            if(count2>0 && sus) {
                Elemente.y2 -= jump;
                count2-=jump;
                repaint();
                if(count2<=0){
                    sus1=false;
                }
            }

    });
    public Kombat() {

        timer.start();
        timer1.start();
        Menu.eliminaActionListeners(6, 11, this);
        Image win1= new ImageIcon("MortalKombat-main/Proiect2/Poze/SWINS.png").getImage();
        Image win2= new ImageIcon("MortalKombat-main/Proiect2/Poze/Zwins.png").getImage();
        Image figure1=new ImageIcon("MortalKombat-main/Proiect2/Poze/SubZero.png").getImage();
        Image figure2= new ImageIcon("MortalKombat-main/Proiect2/Poze/Scorpion.png").getImage();
        Image scaledFigure1, scaledFigure2;
        scaledFigure1 = figure1.getScaledInstance(425, 300, Image.SCALE_SMOOTH);
        scaledFigure2 = figure2.getScaledInstance(300, 300, Image.SCALE_SMOOTH);
        scaledWin1=win1.getScaledInstance(200, 400, Image.SCALE_SMOOTH);
        scaledWin2=win2.getScaledInstance(300, 400, Image.SCALE_SMOOTH);
        Elemente.panels[0]= Alt_Menu.colorare(new ImageIcon("MortalKombat-main/Proiect2/Poze/arena.png").getImage(), scaledFigure1, scaledFigure2);
        healthBar1 =  Menu.configureHealthBar(Names.p1.getName(), health1);
        healthBar2 =  Menu.configureHealthBar(Names.p2.getName(), health2);
        healthBar2.setForeground(Color.RED);
        Elemente.panels[1].add(healthBar1);
        Elemente.panels[1].add(Elemente.butoane[11]);
        Elemente.panels[1].add(healthBar2);

        for(int i=6; i<10; ++i) {
            Elemente.panels[3].add(Elemente.butoane[i]);
        }
        Elemente.panels[2].setLayout(new FlowLayout(FlowLayout.CENTER, 0, 0));
        Elemente.panels[2].add(Elemente.labels[2]);
        Elemente.panels[2].add(Elemente.butoane[10]);


        Elemente.panels[4].setLayout(new GridBagLayout());
        GridBagConstraints gbc =new GridBagConstraints();
        gbc.fill= GridBagConstraints.VERTICAL;
        gbc.anchor=GridBagConstraints.NORTH;
        gbc.gridy=0;
        gbc.gridx=0;
        Elemente.panels[4].add(Elemente.labels[10], gbc);
        Elemente.panels[4].add(Elemente.labels[11], gbc);
        gbc.gridy=1;
        gbc.insets=new Insets(0,0,200,0);
        Elemente.panels[4].add(Elemente.panels[2], gbc);


        Elemente.panels[0].setLayout(new BorderLayout());
        Elemente.panels[0].add(Elemente.panels[1], BorderLayout.NORTH);
        Elemente.panels[0].add(Elemente.panels[4], BorderLayout.CENTER);
        Elemente.panels[0].add(Elemente.panels[3], BorderLayout.SOUTH);
        setContentPane(Elemente.panels[0]);
        setVisible(true);

    }
    public void updateHealth() {

            turn = 1 - turn;

            if(turn==1){
                Elemente.labels[2].setForeground(new Color(0, 200, 255));
                text= Names.p1.getName() + "'s turn ";
            }
            else{
                Elemente.labels[2].setForeground(Color.RED);
                text= Names.p2.getName() + "'s turn ";
            }
            Elemente.labels[2].setText(text);

                int damage = 0;
                int sansa;

                switch (option) {
                    case 1:
                        damage = Player.punch;
                        atac=true;
                        break;
                    case 2:
                        sansa = chance.nextInt(2);
                        if (sansa == 1) {
                            damage = Player.elbow;
                        }
                        atac=true;
                        break;
                    case 3:
                        sansa = chance.nextInt(3);
                        if (sansa == 1) {
                            damage = Player.kick;
                        }
                        atac=true;
                        break;
                    case 4:
                        sansa = chance.nextInt(4);
                        if (sansa == 1) {
                            damage = Player.headbutt;
                        }
                        atac=true;
                        break;
                }

                if (turn == 1) {
                    if(damage==0){
                        Elemente.labels[10].setText(Names.p1.getName()+" dodged ");
                        Elemente.dodged=true;
                        Elemente.labels[10].setForeground(new Color(0, 200, 255));
                        Elemente.labels[10].setVisible(true);
                    }
                    else {
                        health1 = health1 - damage;
                        healthBar1.setValue(health1);

                        if (health1 <= 0) {
                            timer.stop();
                            timer1.stop();
                            new FATALITY(Names.p2.getName(), scaledWin1);
                            dispose();
                            Menu.reset();
                        }
                    }
                    Elemente.labels[11].setVisible(false);
                } else {
                    if(damage==0){
                        Elemente.labels[11].setText(Names.p2.getName()+" dodged ");
                        Elemente.dodged=true;
                        Elemente.labels[11].setVisible(true);

                    }
                    else {
                        health2 = health2 - damage;
                        healthBar2.setValue(health2);
                        if (health2 <= 0) {
                            timer.stop();
                            timer1.stop();
                            new FATALITY(Names.p1.getName(), scaledWin2);
                            dispose();
                            Menu.reset();

                        }
                    }
                    Elemente.labels[10].setVisible(false);
                }


                repaint();
            }




    public void actionPerformed(ActionEvent e) {
        if(Elemente.dodged){
          int step=5;
            if(turn==0){
                if(count<50 && !retras) {
                    Elemente.x2 += step;
                    count+=step;
                    repaint();
                    if(count==50){
                        retras=true;
                    }
                }
                if(count>0 && retras) {
                    Elemente.x2 -= step;
                    count-=step;
                    repaint();
                    if(count==0){
                        retras=false;
                        Elemente.dodged=false;
                    }
                }
            }
            else{
                if(count<50 && !retras) {
                    Elemente.x1 -= step;
                    count+=step;
                    repaint();
                    if(count==50){
                        retras=true;
                    }
                }
                if(count>0 && retras) {
                    Elemente.x1 += step;
                    count-=step;
                    repaint();
                    if(count==0){
                        retras=false;
                        Elemente.dodged=false;
                    }
                }
            }

        }




        if(atac){
            int step=5;
            if(turn==0){
                if(count3<50 && !gata) {
                    Elemente.x1 += step;
                    count3+=step;
                    repaint();
                    if(count3==50){
                        gata=true;
                    }
                }
                if(count3>0 && gata) {
                    Elemente.x1 -= step;
                    count3-=step;
                    repaint();
                    if(count3==0){
                        gata=false;
                        atac=false;
                    }
                }
            }
            else{
                if(count3<50 && !gata) {
                    Elemente.x2 -= step;
                    count3+=step;
                    repaint();
                    if(count3==50){
                        gata=true;
                    }
                }
                if(count3>0 && gata) {
                    Elemente.x2 += step;
                    count3-=step;
                    repaint();
                    if(count3==0){
                        gata=false;
                        atac=false;
                    }
                }
            }

        }



        if(e.getSource()==Elemente.butoane[11]) {
            new Home();
            timer.stop();
            timer1.stop();
            dispose();
            Menu.reset();
        }
        if (e.getSource() == Elemente.butoane[6]) {
            option = 1;
            updateHealth();
        }
        else if (e.getSource() == Elemente.butoane[7]) {
            option = 2;
            updateHealth();
        }
        else if (e.getSource() == Elemente.butoane[8]) {
            option = 3;
            updateHealth();
        }
        else if (e.getSource() == Elemente.butoane[9]) {
            option = 4;
            updateHealth();
        }
        else if(e.getSource()== Elemente.butoane[10]){
            if(turn==1) {
                Elemente.labels[2].setForeground(new Color(0, 200, 255));
                Elemente.labels[2].setText(Names.p1.getName() +"'s turn ");

            }
            else{
                Elemente.labels[2].setForeground(Color.RED);
                Elemente.labels[2].setText(Names.p2.getName() +"'s turn ");

            }
            Elemente.butoane[10].setVisible(false);
        }

    }

}

