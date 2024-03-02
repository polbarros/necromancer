'''Este archivo contiene las clases (modelos) y al usar el ORM las clases serán las tablas de nuestra DB'''

from sqlalchemy import Column, Integer, String, Boolean
import db # Importamos dp.py para poder invocar las variables y clases de allí.

class Login(db.Base): #Hereda de la clase Base del fichero db.py

    __tablename__ = "login"
    __table_args__= {'sqlite_autoincrement': True} #Autoincrementa la PK de la tabla.
    id = Column(Integer, primary_key=True) # Identificador único de jugador.
    name = Column(String(100), nullable=False) # Identificador escogido por el usuario.
    password = Column(String(100), nullable=False) # Contraseña escogida por el usuario.
    max_score = Column(Integer, nullable=False) # Máxima puntuación
    selection = Column(Boolean, nullable=False) # Estado de selección del jugador.

    def __init__(self, name, password, max_score, selection):
        #El id lo crea la BD automáticamente.
        self.name = name
        self.password = password
        self.max_score = max_score
        self.selection = selection
        print("Login creado con éxito")

    def __repr__(self):
        return "El login {}: {} // {}".format(self.id, self.name, self.password)

    def __str__(self):
        return "El login {}: {} // {}".format(self.id, self.name, self.password)

class Warrior(db.Base): #Hereda de la clase Base del fichero db.py

    __tablename__ = "warrior"
    __table_args__ = {'sqlite_autoincrement': True} #Autoincrementa la PK de la tabla.
    id = Column(Integer, primary_key=True) # Identificador único de guerrero.
    name = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)
    exp = Column(Integer, nullable=False)
    hp_max = Column(Integer, nullable=False)
    hp_current = Column(Integer, nullable=False)
    dmg_base = Column(Integer, nullable=False)
    dmg_necrotic = Column(Integer, nullable=False)
    dmg_radiant = Column(Integer, nullable=False)
    bomb = Column(Integer, nullable=False)
    heal = Column(Integer, nullable=False)
    strategy_attack = Column(Boolean, nullable=False)
    power_strike = Column(Boolean, nullable=False)
    res_radiant = Column(Integer, nullable=False)
    res_necrotic = Column(Integer, nullable=False)
    armor = Column(Integer, nullable=False)
    stance = Column(Integer, nullable=False)
    stance_weak = Column(Boolean, nullable=False)
    stance_recovery = Column(Integer, nullable=False)
    attack_roll = Column(Integer, nullable=False)
    roll_recovery = Column(Integer, nullable=False)
    type = Column(String(10), nullable=False)

    def __init__(self, name, level, exp, hp_max, hp_current, dmg_base, dmg_necrotic, dmg_radiant, bomb, heal,
                 strategy_attack, power_strike, res_radiant, res_necrotic, armor, stance, stance_weak, stance_recovery,
                 attack_roll, roll_recovery, type):
        # El id lo crea la BD automáticamente
        self.name = name
        self.level = level
        self.exp = exp
        self.hp_max = hp_max
        self.hp_current = hp_current
        self.dmg_base = dmg_base
        self.dmg_necrotic = dmg_necrotic
        self.dmg_radiant = dmg_radiant
        self.bomb = bomb
        self.heal = heal
        self.strategy_attack = strategy_attack
        self.power_strike = power_strike
        self.res_radiant = res_radiant
        self.res_necrotic = res_necrotic
        self.armor = armor
        self.stance = stance
        self.stance_weak = stance_weak
        self.stance_recovery = stance_recovery
        self.attack_roll = attack_roll
        self.roll_recovery = roll_recovery
        self.type = type
        print("Warrior ready for combat")

    def __repr__(self):
        return "Warrior {}: level {}, with {} HPMax". format(self.id, self.level, self.hp_max)

    def __str__(self):
        return "Warrior {}: level {}, with {} HPMax". format(self.id, self.level, self.hp_max)

