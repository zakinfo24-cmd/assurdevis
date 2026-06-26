import math
from typing import Any

RC_BASE = {4: 3450, 5: 4370, 6: 4830, 7: 5520, 8: 6325, 9: 7475, 10: 8625, 11: 9775, 12: 10925, 13: 12190}
TAUX_CAP = {'00': {'z1': 2.0, 'z2': 1.8}, '02': {'z1': 1.6, 'z2': 1.4}, '06': {'z1': 2.2, 'z2': 2.0}, '07': {'z1': 3.0, 'z2': 2.8}, '36': {'z1': 2.6, 'z2': 2.4}}
GARANTIES = {
    'DR': {'type': 'fixed', 'fixed': 600}, 'DRG': {'type': 'fixed', 'fixed': 400},
    'VIV': {'type': 'pct_valeur', 'pct': 0.01}, 'VOL': {'type': 'pct_valeur', 'pct': 0.006},
    'ICTM': {'type': 'pct_valeur', 'pct': 0.005}, 'BDG': {'type': 'fixed', 'fixed': 2000},
    'EVNA': {'type': 'pct_valeur', 'pct': 0.004}, 'TOPR': {'type': 'pct_valeur', 'pct': 0.035},
    'TR': {'type': 'pct_valeur', 'pct': 0.025}, 'TRC': {'type': 'pct_valeur', 'pct': 0.02},
    'VAN': {'type': 'pct_valeur', 'pct': 0.003}, 'DC10': {'type': 'fixed', 'fixed': 8000},
    'PJX': {'type': 'fixed', 'fixed': 1000}, 'AST': {'type': 'fixed', 'fixed': 1500},
    'ASTP': {'type': 'fixed', 'fixed': 3000}, 'BGP': {'type': 'fixed', 'fixed': 2500},
    'RVF': {'type': 'pct_valeur', 'pct': 0.005}, 'VN': {'type': 'pct_valeur', 'pct': 0.008},
    'EMP': {'type': 'pct_valeur', 'pct': 0.002}, 'TOP2': {'type': 'fixed', 'fixed': 500},
    'OPT': {'type': 'fixed', 'fixed': 1000}, 'TMP': {'type': 'fixed', 'fixed': 800},
    'IRCC': {'type': 'pct_valeur', 'pct': 0.008},
}
USAGE_COEF = {'personnel': 1.0, 'professionnel': 1.4}
RO_CODES = ['RC', 'DR', 'DRG', 'AST', 'ASTP']
DUREES = {1: 0.12, 3: 0.3, 6: 0.55, 9: 0.8, 12: 1.0}
CONDUCTEUR = {'capital': 200000, 'taux': 0.005}

TAUX_RD = {
    'catnat': {'label': 'CAT-NAT', 'taux_pml': 0.8, 'obligatoire': True},
    'incendie': {'label': 'Incendie', 'taux_pml': 1.5, 'obligatoire': True},
    'mrh': {'label': 'Multirisque Habitation', 'taux_pml': 1.2, 'obligatoire': False},
    'rcpro': {'label': 'RC Pro', 'taux_pml': 0.8, 'obligatoire': True},
    'decennale': {'label': 'Décennale', 'taux_pml': 2.0, 'obligatoire': True},
    'trc': {'label': 'TRC', 'taux_pml': 1.8, 'obligatoire': True},
    'transport': {'label': 'Transport', 'taux_pml': 0.8, 'obligatoire': True},
    'accidents': {'label': 'Accidents', 'taux_pml': 0.5, 'obligatoire': False},
    'rcgenerale': {'label': 'RC Générale', 'taux_pml': 0.6, 'obligatoire': False},
    'credit': {'label': 'Crédit', 'taux_pml': 1.2, 'obligatoire': False},
    'recoltes': {'label': 'Récoltes', 'taux_pml': 1.0, 'obligatoire': False},
    'cyber': {'label': 'Cyber', 'taux_pml': 2.0, 'obligatoire': False},
}


def calc_auto(fields: dict) -> dict | None:
    valeur = float(fields.get('valeur', 0))
    if valeur <= 0:
        return None
    cv = int(fields.get('puissance', 7))
    genre = fields.get('genre', '00')
    zone = int(fields.get('zone', 1))
    usage = fields.get('usage', 'personnel')
    garanties = fields.get('garanties', ['RC'])
    age = int(fields.get('age', 0))
    duree_mois = int(fields.get('duree_mois', 12))
    reduction = float(fields.get('reduction', 0))

    usage_coeff = USAGE_COEF.get(usage, 1.0)
    rc = round(RC_BASE.get(cv, 5520) * usage_coeff)
    cap_info = TAUX_CAP.get(genre, TAUX_CAP['00'])
    taux_cap = cap_info['z2'] if zone > 1 else cap_info['z1']
    cap = round(valeur * taux_cap / 100)
    rc = min(rc, cap)

    items = [{'label': 'RC Responsabilité Civile', 'value': rc, 'code': 'RC', 'type': 'RO'}]
    total_ro = rc
    total_rno = 0
    rno_items = []

    dc_montant = float(fields.get('dc_montant', 0))
    dc_franchise = float(fields.get('dc_franchise', 0))
    if dc_montant > 0:
        dc_label = f'Dommages Collision (franchise {dc_franchise:,.0f} DA)' if dc_franchise > 0 else 'Dommages Collision'
        items.append({'label': dc_label, 'value': round(dc_montant), 'code': 'DC', 'type': 'RNO'})
        total_rno += round(dc_montant)
        rno_items.append({'code': 'DC', 'value': round(dc_montant)})

    label_map = {'VIV': 'Vol & Incendie', 'BDG': 'Bris de Glaces', 'TOPR': 'Tous Risques (Omnium)', 'TR': 'Tous Risques', 'DC10': 'Dommage Collision', 'DR': 'Défense & Recours', 'VOL': 'Vol', 'ICTM': 'Incendie/Tempête', 'EVNA': 'Événements Naturels', 'VAN': 'Vandalisme', 'AST': 'Assistance', 'PJX': 'Perte de Jouissance', 'VN': 'Valeur à Neuf'}
    for g in garanties:
        if g == 'RC':
            continue
        gin = GARANTIES.get(g)
        if not gin:
            continue
        if gin['type'] == 'fixed':
            m = gin['fixed']
        elif gin['type'] == 'pct_valeur':
            m = round(valeur * gin['pct'])
        else:
            continue
        if m > 0:
            is_ro = g in RO_CODES
            items.append({'label': label_map.get(g, g), 'value': m, 'code': g, 'type': 'RO' if is_ro else 'RNO'})
            if is_ro:
                total_ro += m
            else:
                total_rno += m
                rno_items.append({'code': g, 'value': m})

    reduction_amount = 0
    if reduction > 0 and total_rno > 0:
        reduction_amount = round(total_rno * reduction / 100)
        items.append({'label': f'Réduction {reduction}%', 'value': -reduction_amount, 'code': 'REDUC', 'type': 'REDUCTION'})
    total_rno_net = total_rno - reduction_amount
    pc = round(CONDUCTEUR['capital'] * CONDUCTEUR['taux'])
    items.append({'label': 'Ind. Conducteur', 'value': pc, 'code': 'COND', 'type': 'FIXE'})
    total = total_ro + total_rno_net + pc

    jeune = fields.get('jeune_conducteur', 'non')
    if jeune == 'oui' or (age > 0 and age < 25):
        jeune_taux = 0.25 if (age > 0 and age < 21) else 0.15
        s = round(total * jeune_taux)
        items.append({'label': f'Surprime {"-21" if age < 21 else "-25"} ans', 'value': s, 'code': 'JEUNE', 'type': 'FIXE'})
        total += s
    if fields.get('permis_recent') == 'oui':
        s = round(total * 0.10)
        items.append({'label': 'Surprime permis récent', 'value': s, 'code': 'PERMIS', 'type': 'FIXE'})
        total += s

    coef = DUREES.get(duree_mois, 1.0)
    total = round(total * coef)
    fga = round(total * 0.03)
    tva = round(total * 0.19)
    total_ttc = total + tva + fga
    monthly = round(total_ttc / 12)

    return {
        'items': items,
        'total_ht': total,
        'tva': tva,
        'fga': fga,
        'total_ttc': total_ttc,
        'monthly': monthly,
        'reduction_applied': reduction if reduction > 0 else 0,
        'reduction_amount': reduction_amount,
        'duree_mois': duree_mois,
        'garanties': garanties,
    }


def calc_rd(fields: dict) -> dict | None:
    branche = fields.get('branche_rd', 'incendie')
    valeur = float(fields.get('valeur_bien', fields.get('valeur', 0)))
    if valeur <= 0:
        return None
    meta = TAUX_RD.get(branche, TAUX_RD['incendie'])
    taux = (meta['taux_pml'] or 1.5) / 1000
    total_ht = round(valeur * taux)
    fga = round(total_ht * 0.03)
    tva = round(total_ht * 0.19)
    total_ttc = total_ht + tva + fga
    monthly = round(total_ttc / 12)
    return {
        'branche': branche,
        'label': meta['label'],
        'obligatoire': meta['obligatoire'],
        'total_ht': total_ht,
        'tva': tva,
        'fga': fga,
        'total_ttc': total_ttc,
        'monthly': monthly,
        'items': [
            {'label': f"Prime {meta['label'] or branche}", 'value': total_ht, 'code': 'PRIME', 'type': 'HT'},
            {'label': 'TVA 19%', 'value': tva, 'code': 'TVA', 'type': 'TAXE'},
            {'label': 'FGA 3%', 'value': fga, 'code': 'FGA', 'type': 'TAXE'},
        ],
    }
