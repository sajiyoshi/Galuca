カーネギーメロン大学のLuca Damascoさんが作ったGalucaというゲーム(2015)をRaspberry PiやRaspberry Pi Desktop（PC/Mac）の環境で動かせるようにしました。Python２でPygameを使って書かれています。元々はGalaga（ギャラガ）というアーケードゲームのリメイクです。タイトーのスペース・インベーダー(1978)大ヒットに続いてナムコが送り出したGalaxian(1979), Galaga(1981), Gaplus(1984)３部作の２作目に当たります。フルカラー化、編隊を組んでの降下攻撃などスペース・インベーダーから大幅にアップデートされたシューティングゲーム黎明期の名作です。

カーネギーメロン大学のプログラミング初学者向け講座での課題で制作されたようで、敵機の襲来パターンをカスタマイズできる機能が追加されています。

緑色のClone or downloadボタン -> Download ZIPのあと、以下のコマンドで起動します。
```
$ unzip Galuca-master.zip
$ cd Galuca-master
$ python Galuca-Final.py
```
----------------------------------------


これは、GALUCAのREADMEです
 これは、***Luca Damasco***によって作られました。
----------------------------------------
Galuca was created as a term project for Carnegie Mellon
University's Introduction to Programming class 15-112. It
is meant to replicate the fixed shooter arcade game Galaga
(originally published in 1981 by Namco and Midway). It also aims
to allow user to customize their gaming experience by creating their own
enemies movement paths. Main complexities include
determining movement patterns of enemies based on the location of the 
fighter, movement of enemies in formation, and translation of user 
generated paths and sprites into functional game movement algorithms. 
 
Programming Language:
	Python 2.7 32 bit
	#Pygame 1.9 only has 32 bit support and will not run with 64 bit versions. 

Module's Used: 
	Pygame 1.9
		Downloaded from Pygame.Org
		The pygame audio mixer was also used. (packaged with pygame 1.9) 
		Instructional materials used were found on Pygame.org and Youtube.com
		(Tutorials from "thenewboston")

CopyRight notices:
	Sprites are from Namco-Midway's GALAGA

	Sprite Materials were "ripped" by JDASTERE4
	(Found on google images when searching "Galaga Sprite Sheets")

	Sounds are from Namco-Midway's GALAGA
	Sounds were purchased from iTunes under "Galaga" by NAMCO SOUNDS

	Logo Materials taken from:
	http://gamingbolt.com/tag/galaga

	Starting Screen Music from:
	"Galaga Remix Demo"
	http://www.newgrounds.com/audio/listen/265069
	Created by "ArcX"
	

All copyrighted materials have been used for educational purposes only 
and are protected under fair use.  

Reference Notices:
    Pygame, image centered rotation code referenced from : 
		http://www.pygame.org/wiki/RotateCenter
	
Controls : 
Arrow Keys (Left and Right) to move
SPACE Key to shoot
Mouse controls for start screen UI

To reset HiScores, delete every line from the "hiScores.txt" 
file except the first line 20,000. DO NOT LEAVE IT BLANK!
