from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.alert_rule import AlertRuleCreate, AlertRuleUpdate, AlertRuleRead
from app.services import alert_rule

router = APIRouter(prefix="/alert-rules", tags=["Alert Rules"])

@router.post("/", response_model=AlertRuleRead)
def create(rule: AlertRuleCreate, db: Session = Depends(get_db)):
    return alert_rule.create_alert_rule(db, rule)

@router.get("/", response_model=list[AlertRuleRead])
def list_rules(db: Session = Depends(get_db)):
    return alert_rule.list_alert_rules(db)

@router.get("/{rule_id}", response_model=AlertRuleRead)
def get(rule_id: int, db: Session = Depends(get_db)):
    return alert_rule.get_alert_rule(db, rule_id)

@router.put("/{rule_id}", response_model=AlertRuleRead)
def update(rule_id: int, rule: AlertRuleUpdate, db: Session = Depends(get_db)):
    return alert_rule.update_alert_rule(db, rule_id, rule)

@router.delete("/{rule_id}")
def delete(rule_id: int, db: Session = Depends(get_db)):
    alert_rule.delete_alert_rule(db, rule_id)
    return {"detail": "Deleted"}

@router.post("evaluate/{snapshot_id}")
def evaluate(snapshot_id: int, db: Session = Depends(get_db)):
    alert_rule.evaluate_rules_and_generate_alerts(db, snapshot_id)
    return {"detail": f"Evaluated rules for snapshot {snapshot_id}"}