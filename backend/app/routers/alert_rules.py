from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.aler_rule import AlertRuleCreate, AlertRuleUpdate, AlertRuleRead
from app.services import alert_rule, rule_service

router = APIRouter(prefix="alert-rules", tags=["Alert Rules"])

@router.post("/", response_model=AlertRuleRead)
def create(rule: AlertRuleCreate, db: Session = Depends(get_db)):
    return rule_service.create_alert_rule(db, rule)

@router.get("/", response_model=list[AlertRuleRead])
def list_rules(db: Session = Depends(get_db)):
    return rule_service.list_alert_rules(db)

@router.get("/{rule_id}", response_model=AlertRuleRead)
def get(rule_id: int, db: Session = Depends(get_db)):
    return rule_service.get_alert_rule(db, rule_id)

@router.put("/{rule_id}", response_model=AlertRuleRead)
def update(rule_id: int, rule: AlertRuleUpdate, db: Session = Depends(get_db)):
    return rule_service.update_alert_rule(db, rule_id, rule)

@router.delete("/{rule_id}")
def delete(rule_id: int, db: Session = Depends(get_db)):
    rule_service.delete_alert_rule(db, rule_id)
    return {"detail": "Deleted"}

@router.post("evaluate/{snapshot_id}")
def evaluate(snapshot_id: int, db: Session = Depends(get_db)):
    rule_service.evaluate_rules_and_generate_alerts(db, snapshot_id)
    return {"detail": f"Evaluated rules for snapshot {snapshot_id}"}