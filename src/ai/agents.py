def format_evidence_response(evidence):
    # Enforce safe formatting
    
    domain = evidence.get("domain", "")
    sig = evidence.get("signal", "").replace("_", " ").title()
    ev_level = evidence.get("evidence_level", "UNKNOWN")
    interp = evidence.get("interpretation", "")
    caveat = evidence.get("caveat", "")
    pe = evidence.get("primary_evidence", {})
    val = evidence.get("validation", {})
    
    if domain == "MARKET":
        return f"""### Answer
{sig} is a top skill demanded in the market.

### Why it matters
{interp}

<details>
<summary><b>View Evidence</b></summary>
<br>
<b>Domain:</b> {domain}<br>
<b>Signal:</b> {sig}<br>
<b>Evidence Level:</b> {ev_level}<br>
<b>Method:</b> {pe.get('model')}<br>
<b>Caveat:</b> {caveat}<br>
<b>Source:</b> Market Data
</details>
"""

    return f"""### Answer
{sig} has {ev_level} statistical evidence as a {domain} capability signal.

### Why it matters
{interp}

<details>
<summary><b>View Evidence</b></summary>
<br>
<b>Domain:</b> {domain}<br>
<b>Signal:</b> {sig}<br>
<b>Evidence Level:</b> {ev_level}<br>
<b>Model:</b> {pe.get('model', 'Logistic Regression')}<br>
<b>Odds Ratio:</b> {pe.get('odds_ratio', 'N/A')} (95% CI: [{pe.get('ci_lower', 'N/A')}, {pe.get('ci_upper', 'N/A')}])<br>
<b>p-value:</b> {pe.get('p_value', 'N/A')}<br>
<b>CV AUC:</b> {val.get('cv_auc', 'N/A')}<br>
<b>Caveat:</b> {caveat}
</details>
"""

def evidence_explainer(query, context):
    if not context:
        return "I do not have validated evidence for that in the supplied datasets."
        
    response = ""
    for ev in context:
        response += format_evidence_response(ev) + "\\n---\\n"
    return response

def career_navigator(query, context):
    if not context:
        return "I do not have validated evidence for that in the supplied datasets. Please specify a recognized skill or trait."
        
    return "Based on the validated evidence:\\n\\n" + evidence_explainer(query, context)

def curriculum_planner(query, context):
    if not context:
        return "I do not have validated evidence for that in the supplied datasets."
        
    resp = "### Learning Priorities Based on Evidence\\n\\n"
    for ev in context:
        domain = ev.get("domain")
        sig = ev.get("signal", "").replace("_", " ").title()
        
        if domain == "MARKET":
            resp += f"**MARKET DEMAND:** {sig} is a high-priority candidate based on the available market evidence.\\n"
        elif domain == "JDS":
            resp += f"**CAPABILITY EVIDENCE:** {sig} is a high-priority candidate based on the available JDS outcome evidence.\\n"
        
    resp += "\\n" + evidence_explainer(query, context)
    return resp

def opportunity_radar(query, context):
    if not context:
        return "I do not have validated evidence for that in the supplied datasets."
        
    resp = "### Market Opportunities\\n"
    for ev in context:
        if ev.get("domain") == "MARKET":
            resp += f"- {ev.get('signal').title()}: {ev.get('interpretation')}\\n"
    if resp == "### Market Opportunities\\n":
        resp += "No specific market signals found for your query. Here is related outcome evidence:\\n\\n"
        resp += evidence_explainer(query, context)
    return resp
