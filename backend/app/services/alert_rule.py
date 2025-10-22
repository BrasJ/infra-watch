from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.db.models.alert_rule import AlertRule
from app.db.models.metric import Metric
from app.db.models.alert import Alert
from app.schemas.alert_rule import AlertRuleCreate, AlertRuleUpdate
from app.schemas.alert import AlertSeverity

def create_alert_rule(db: Session, rule_data: AlertRuleCreate) -> AlertRule:
    rule = AlertRule(**rule_data.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def list_alert_rules(db: Session) -> List[AlertRule]:
    return db.query(AlertRule).all()

def get_alert_rule(db: Session, rule_id: int) -> AlertRule:
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    return rule

def update_alert_rule(db: Session, rule_id: int, rule_data: AlertRuleUpdate) -> AlertRule:
    rule: get_alert_rule(db, rule_id)
    for field, value in rule_data.model_dump().items():
        setattr(rule, field, value)
    db.commit()
    db.refresh(rule)
    return rule

def delete_alert_rule(db: Session, rule_id: int):
    rule = get_alert_rule(db, rule_id)
    db.delete(rule)
    db.commit()

def evaluate_rules_and_generate_alerts(db: Session, snapshot_id: int):
    rules = db.query(AlertRule).filter(AlertRule.enabled == True).all()
    metrics = db.query(Metric).filter(Metric.snapshot_id == snapshot_id).all()

    for rule in rules:
        for metric in metrics:
            if rule.metric_name != metric.name:
                continue
            if rule.host_id and rule.host_id != metric.host_id:
                continue

            if eval(f"{metric.value} {rule.operator} {rule.threshold}"):
                new_alert = Alert(
                    snapshot_id=snapshot_id,
                    host_id=metric.host_id,
                    message=rule.message,
                    severity=rule.severity,
                    type="auto",
                    acknowledged=False,
                )
                db.add(new_alert)
    db.commit()