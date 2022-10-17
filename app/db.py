from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.app= app
        from app.models import material
        from app.models import pedido
        from app.models import proovedor
        db.drop_all()
        db.create_all()
        seed()

def seed():
    from app.models.material import Material
    m1= Material("Plástico de alto índice", "Los lentes más delgados y livianos disponibles. Son altamente recomendados  si tienes prescripción alta para gafas, para miopía, hipermetropía y astigmatismo")
    m2= Material("Policarbonato", "Lentes livianos que son excesivamente resistentes al impacto y ofrecen además protección UV. Una opción apta para los niños y los lentes de seguridad.")
    m3= Material("Trivex", "Similares a los lentes de policarbonato, los lentes Trivex son delgados, livianos,  mucha más resistencia al impacto que los lentes de plástico regulares. Sin embargo, ofrecen visión nítida y un valor Abbe mayor a los lentes de policarbonato")
    m4= Material("Plástico CR-39", " Estos lentes tienen la mitad del peso de los lentes de vidrio pero ofrecen la excelente corrección de la visión; sin embargo, son generalmente más gruesos que las opciones en plástico.")
    m5= Material("Vidrio Crown", "Los lentes de vidrio ofrecen siempre  la mejor experiencia óptica ya que el vidrio refracta la luz mucho más eficientemente que el plástico, sin embargo, son más pesados y gruesos que las opciones en plástico.")
    m6= Material("Titanio", "Un metal muy usado en tecnología aeronáutica y espacial por su alta resistencia y para la fabricación de anteojos se usa en aleaciones para imprimir solidez.")
    m7= Material("Cobalto", "Otro metal con el que se fabrican armazones ligeros, flexibles y muy resistentes porque no es corrosivo.")
    m8= Material("Oro", "Los armazones que se elaboran con este metal suelen ser los más codiciados por su alto valor y procesos de calidad")
    m9= Material("Acetato", "Es una opción creativa y muy conveniente en cuanto a precio en los productos para la visión, y es extremadamente liviana")
    m10= Material("Zyl", "Es fácil de teñir en muchos colores diferentes y es ligero, así como hipoalergénico")
    
    from app.models.proovedor import Proovedor
    p1= Proovedor("Juan Perez", "reciclador", m1, 20000)
    p2= Proovedor("Marcos Gomez", "reciclador", m2, 20000)
    p3= Proovedor("María Ramírez", "fabricante", m3, 20000)
    p4= Proovedor("Juana Lopez", "reciclador", m4, 20000)
    p5= Proovedor("Pedro Rodriguez", "fabricante", m5, 20000)

        
    for proovedor in [p1,p2,p3,p4,p5]:
        db.session.add(proovedor)

    
    db.session.commit()