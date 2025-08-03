import sys
import os

# Προσθήκη του root directory στο path για να λειτουργούν σωστά τα imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.core.orchestrator import OrchestratorAgent

def main():
    """
    Η κύρια συνάρτηση που εκτελεί τη διαδραστική ροή εργασίας.
    """
    # 1. Λήψη Αρχικού Θέματος
    topic = input("🔥 Για ποιο γενικό θέμα θέλεις να μιλήσουμε; ")
    initial_state = {"topic": topic}

    # 2. Εκκίνηση του Orchestrator και Ανάλυση Τάσεων
    orchestrator = OrchestratorAgent()

    print("\n--- 📈 Αναλύω τις τρέχουσες τάσεις για το θέμα σου... ---")
    state_with_trends = orchestrator.trend_analysis_agent.invoke(initial_state)
    trend_report = state_with_trends.get("trend_analysis_report")

    if trend_report and "Error:" not in trend_report:
        print("\n--- 📊 Αναφορά Τάσεων ---")
        print(trend_report)
        print("--------------------------")
    else:
        print("\n⚠️ Δεν ήταν δυνατή η ανάλυση των τάσεων. Προχωράμε χωρίς αυτή την πληροφορία.")

    # 3. Διαδραστική Δημιουργία Creative Brief
    state_with_brief = orchestrator.client_briefing_agent.invoke(state_with_trends)
    creative_brief = state_with_brief.get("creative_brief")

    # Αν ο χρήστης ακυρώσει ή το brief αποτύχει, σταμάτα.
    if not creative_brief or "Error:" in creative_brief:
        print("\n❌ Η διαδικασία δημιουργίας brief δεν ολοκληρώθηκε. Το πρόγραμμα θα τερματιστεί.")
        return

    # 4. Δημιουργία Ιδεών Περιεχομένου με βάση το Brief
    print("\n--- 🤔 Δημιουργώ ιδέες για περιεχόμενο με βάση τη στρατηγική μας... ---")
    state_with_ideas = orchestrator.content_strategy_agent.invoke(state_with_brief)
    ideas = state_with_ideas.get("ideas")

    # 5. Διαδραστική Επιλογή Ιδέας
    if not ideas or not isinstance(ideas, list):
        print("\n😕 Δυστυχώς, δεν κατάφερα να βρω σχετικές ιδέες. Δοκίμασε ένα διαφορετικό θέμα.")
        return

    print("\n✨ Βρήκα τις παρακάτω ιδέες για εσένα:")
    for i, idea in enumerate(ideas):
        print(f"  {i + 1}. {idea}")
    print("  0. Καμία από τις παραπάνω. Έξοδος.")

    selected_idea = None
    while True:
        try:
            choice = int(input("\n👉 Διάλεξε τον αριθμό της ιδέας που προτιμάς: "))
            if 0 <= choice <= len(ideas):
                if choice == 0:
                    print("\n👍 Κατανοητό. Καλύτερα να μην προχωρήσουμε. Τα λέμε!")
                    return
                selected_idea = ideas[choice - 1]
                break
            else:
                print(f"Λάθος επιλογή. Διάλεξε έναν αριθμό από το 0 έως το {len(ideas)}.")
        except ValueError:
            print("Παρακαλώ, δώσε μόνο τον αριθμό.")

    # 6. Δημιουργία Τελικού Περιεχομένου
    print(f"\n✅ Εξαιρετική επιλογή! Ετοιμάζω το περιεχόμενο για την ιδέα: '{selected_idea}'")
    writing_state = {**state_with_ideas, "selected_idea": selected_idea}
    final_state = orchestrator.content_writer_agent.invoke(writing_state)

    # 7. Εκτύπωση Κειμένου & Δημιουργία Οπτικών Προτάσεων
    print("\n--- ✍️ Το Τελικό σου Περιεχόμενο ---")
    final_content = final_state.get("final_content", "Δεν δημιουργήθηκε περιεχόμενο.")
    print(final_content)
    print("-------------------------------------")

    # 8. Δημιουργία και Επιλογή Οπτικών Προτάσεων
    print("\n--- 🎨 Προτάσεις για Εικόνες ---")
    state_with_visuals = orchestrator.visual_suggestion_agent.invoke(final_state)
    visual_suggestions = state_with_visuals.get("visual_suggestions", [])

    if not visual_suggestions:
        print("Δεν βρέθηκαν οπτικές προτάσεις.")
    else:
        for i, suggestion in enumerate(visual_suggestions):
            print(f'\n{i+1}. {suggestion["description"]}')
        
        print("---------------------------------")
        
        # 9. Διαδραστική Επιλογή και Δημιουργία Εικόνας
        choice = input(f"🖼️ Διάλεξε εικόνα για δημιουργία (1-{len(visual_suggestions)}) ή πάτα 'K' για καμία: ").strip().lower()

        if choice.isdigit() and 1 <= int(choice) <= len(visual_suggestions):
            selected_prompt = visual_suggestions[int(choice) - 1]["prompt"]
            print(f"\n🚀 Επιλέχθηκε το prompt: '{selected_prompt}'. Ξεκινά η δημιουργία εικόνας...")
            
            image_state = {"image_prompt": selected_prompt}
            final_image_state = orchestrator.image_generation_agent.invoke(image_state)
            image_path = final_image_state.get("image_path", "Η δημιουργία απέτυχε.")

            print("\n--- ✨ Αποτέλεσμα Εικόνας ---")
            print(f"Η εικόνα σου αποθηκεύτηκε εδώ: {image_path}")
            print("---------------------------")
        else:
            print("\n👍 ΟΚ, δεν θα δημιουργηθεί εικόνα.")
    print("\n========================================")
    print("✅ Η δημιουργία περιεχομένου ολοκληρώθηκε!")
    print("========================================")
    print("\nΠροτεινόμενη Ανάρτηση:")
    print("--------------------")
    print(final_content)
    print("--------------------\n")

if __name__ == "__main__":
    main()
