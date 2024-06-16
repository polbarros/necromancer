# Necromancer

### Description
Necromancer is a video game made with PyGame for the purpose of completing and presenting a final Python programming 
project for the TokioSchool course.

The project must meet a series of minimum requirements to be considered complete: it must contain a Login system, 
use object-oriented programming, and handle SQL-type databases. However, the choice to create a digital entertainment 
product was free and stems from my passion for video games and the need to undertake projects with creative and even 
artisanal elements.

The initial idea of Necromancer was to create a video game to be played in parallel while performing other tasks on 
the computer. In many offices, most workers must spend long hours in front of the computer operating with different 
types of content. However, maintaining attention on a single source of stimuli is a challenge, and we often fail in 
that endeavor. Failing to maintain concentration can have negative consequences and lead workers to make mistakes in 
their work. Therefore, Necromancer aims to be a low-profile distraction that allows us to "decompress" our focus to 
refresh our capabilities at times when we deem it appropriate.

To achieve this goal, Necromancer has reduced window dimensions, a vertical aspect ratio, and its pace is determined 
by the player, as it consists of consecutive turn-based duels, whose action does not advance unless the player desires it.

In Necromancer, the player must take on the role of a dark wizard capable of reviving warriors fallen in battle 
to continue fighting against the Shogun's servants and forest creatures. After choosing one of four possible warriors, 
the player progresses through a series of duels where they will test their strategic abilities, the unique skills of 
the undead they control, and the luck provided by the dice. After each victory, the player is rewarded with prizes that 
allow them to improve their offensive or defensive conditions and thus defeat as many enemies as possible.

### Requirements
SQLAlchemy~=2.0.22 

pygame~=2.5.2

### Installation

1. Clone this repository:
```bash
git clone https://github.com/polbarros/necromancer.git
cd necromancer
```
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # In Windows use `venv\Scripts\activate`
```
3. Install requirements:
```bash
pip install -r requirements.txt
```

### Author
Pol Barrós