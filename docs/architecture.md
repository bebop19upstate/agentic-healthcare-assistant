# Architecture

## Component overview

See the diagram and phased plan for the full component table. This document
captures the request lifecycle traced during Phase 5, before LangGraph wiring
began in Phase 6.

## Request lifecycle: the sample scenario

**Input query:** "My 70-year-old father has chronic kidney disease. I want to
book a nephrologist for him. Also, can you summarize latest treatment methods?"

1. **Planner** (src/planner.py) receives the query, returns a Plan with 3 subtasks:
   - "Retrieve medical history" → tool: ehr
   - "Book nephrologist appointment" → tool: appointment
   - "Summarize latest treatment methods" → tool: disease_search

2. **EHR subtask**: get_patient_history(1) fetches John Doe Sr.'s record.
   memory_manager.get_context(1, query) pulls relevant prior context, if any.
   EHR_SUMMARY_PROMPT summarizes the record into 1-2 sentences.
   → Result: "John Doe Sr., 70, has stage 3 CKD."

3. **Appointment subtask**: find_slots("nephrology") returns available slots.
   book_slot(1, chosen_slot) books the first available nephrology slot.
   → Result: "Booked with Dr. Rao for [date/time]."

4. **Disease search subtask**: search_disease_info("latest CKD treatment methods")
   retrieves relevant chunks from the disease corpus and generates a grounded
   answer using DISEASE_ANSWER_PROMPT.
   → Result: grounded summary of CKD treatment options (ACE inhibitors, SGLT2
   inhibitors, monitoring, etc.)

5. **Composer**: all 3 results are combined via COMPOSER_PROMPT into one
   final, coherent reply mentioning the booking, a brief mention of the
   patient's condition, and the treatment summary — written naturally, not
   as three disconnected paragraphs.

## What Phase 6 needs to build

- A shared state object carrying: query, patient_id, plan, tool_results, final_answer
- One node per stage above (planner_node, ehr_node, appointment_node,
  disease_search_node, composer_node)
- Routing logic so only the subtasks the planner identified actually run
  (e.g. a booking-only query should never call disease_search_node)

## Phase 7 test scenarios

1. **Booking-only** — "Book me a cardiologist appointment next week."
   Expect: only appointment tool runs; final answer discusses only the booking.

2. **EHR-update-only** — "Add a note to my father's record: started a new
   blood pressure medication."
   Expect: only EHR tool runs; record is actually updated in the database;
   final answer confirms the update.

3. **Disease-info-only** — "What's the latest on kidney disease treatment?"
   Expect: only disease_search runs; grounded answer; no unrelated content.

4. **Unknown patient** — query references a patient_id not in the database.
   DECISION: the system stops entirely and reports the patient couldn't be
   found — it does NOT attempt booking or disease-search even if those parts
   of the query would otherwise be valid, since a request about an
   unidentifiable patient shouldn't partially proceed.

5. **Ambiguous query** — "I need help," no clear tool mapping.
   DECISION: the composer must explicitly ask "Could you tell me more about
   what you need?" rather than a generic non-answer or a fabricated response.
