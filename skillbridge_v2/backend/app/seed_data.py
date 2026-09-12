from app.database import SessionLocal, engine, Base
from app.models import Branch, Skill, Internship

def seed():
    print("Creating all tables in PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Branches
        branches = [
            Branch(id="cse", name="Computer Science & Engineering"),
            Branch(id="ece", name="Electronics & Communication Engineering"),
            Branch(id="mech", name="Mechanical Engineering"),
            Branch(id="eee", name="Electrical & Electronics Engineering"),
        ]
        for b in branches:
            if not db.query(Branch).filter_by(id=b.id).first():
                db.add(b)
        db.commit()
        print("✓ Branches seeded (CSE, ECE, MECH, EEE)")

        # 2. Seed Skills per Branch
        skills_data = [
            # Universal
            {"id": "python", "name": "Python", "domain": "General", "branch_id": None, "is_universal": True},
            {"id": "git", "name": "Git & GitHub", "domain": "General", "branch_id": None, "is_universal": True},
            {"id": "c_prog", "name": "C Programming", "domain": "General", "branch_id": None, "is_universal": True},

            # CSE
            {"id": "react", "name": "React.js", "domain": "Web Development", "branch_id": "cse", "is_universal": False},
            {"id": "fastapi", "name": "FastAPI", "domain": "Backend", "branch_id": "cse", "is_universal": False},
            {"id": "sql", "name": "PostgreSQL / SQL", "domain": "Database", "branch_id": "cse", "is_universal": False},
            {"id": "pytorch", "name": "PyTorch", "domain": "AI/ML", "branch_id": "cse", "is_universal": False},
            {"id": "docker", "name": "Docker", "domain": "DevOps", "branch_id": "cse", "is_universal": False},

            # ECE
            {"id": "verilog", "name": "Verilog HDL", "domain": "VLSI Design", "branch_id": "ece", "is_universal": False},
            {"id": "embedded_c", "name": "Embedded C", "domain": "Firmware", "branch_id": "ece", "is_universal": False},
            {"id": "rtos", "name": "FreeRTOS", "domain": "Embedded Systems", "branch_id": "ece", "is_universal": False},
            {"id": "arm_cortex", "name": "ARM Cortex-M", "domain": "Hardware Architecture", "branch_id": "ece", "is_universal": False},
            {"id": "comm_protocols", "name": "I2C / SPI / UART", "domain": "Hardware Protocols", "branch_id": "ece", "is_universal": False},

            # MECH
            {"id": "solidworks", "name": "SolidWorks", "domain": "CAD/CAM", "branch_id": "mech", "is_universal": False},
            {"id": "catia", "name": "CATIA", "domain": "CAD Design", "branch_id": "mech", "is_universal": False},
            {"id": "ansys", "name": "ANSYS FEA", "domain": "Finite Element Analysis", "branch_id": "mech", "is_universal": False},
            {"id": "gdt", "name": "GD&T", "domain": "Manufacturing", "branch_id": "mech", "is_universal": False},
            {"id": "cnc", "name": "CNC Programming", "domain": "Machining", "branch_id": "mech", "is_universal": False},

            # EEE
            {"id": "simulink", "name": "Simulink & MATLAB", "domain": "Control Systems", "branch_id": "eee", "is_universal": False},
            {"id": "plc_scada", "name": "PLC & SCADA", "domain": "Industrial Automation", "branch_id": "eee", "is_universal": False},
            {"id": "power_electronics", "name": "Power Electronics", "domain": "Power Systems", "branch_id": "eee", "is_universal": False},
            {"id": "pcb_design", "name": "KiCAD / Altium PCB", "domain": "Hardware Interfacing", "branch_id": "eee", "is_universal": False},
        ]

        for s in skills_data:
            if not db.query(Skill).filter_by(id=s["id"]).first():
                db.add(Skill(**s))
        db.commit()
        print(f"✓ Seeded {len(skills_data)} skills across branches")

        # 3. Seed Sample Cross-Branch Internships
        if not db.query(Internship).first():
            internships = [
                Internship(
                    company_name="Qualcomm",
                    title="Embedded Firmware Intern",
                    description="Work on real-time embedded firmware and peripheral device drivers.",
                    eligible_branches="ece,cse",
                    min_readiness_score=60.0
                ),
                Internship(
                    company_name="Tesla",
                    title="CAD Modeling & Structural Intern",
                    description="Responsible for 3D modeling, GD&T drawings, and structural FEA simulations.",
                    eligible_branches="mech",
                    min_readiness_score=50.0
                ),
                Internship(
                    company_name="Schneider Electric",
                    title="Industrial Automation & Control Intern",
                    description="Work with PLC/SCADA configurations and motor drive control circuits.",
                    eligible_branches="eee",
                    min_readiness_score=55.0
                ),
                Internship(
                    company_name="Razorpay",
                    title="Backend Software Intern",
                    description="Design scalable microservices using Python, FastAPI, and PostgreSQL.",
                    eligible_branches="cse,ece",
                    min_readiness_score=65.0
                )
            ]
            db.add_all(internships)
            db.commit()
            print("✓ Sample internships seeded")

        print("\nAll database tables and seed rows created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()