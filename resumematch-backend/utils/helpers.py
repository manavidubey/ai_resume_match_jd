from typing import List, Dict, Any
import math


def calculate_weighted_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Calculate weighted score based on multiple criteria
    """
    total_weighted_score = 0.0
    total_weights = 0.0
    
    for criterion, score in scores.items():
        if criterion in weights:
            total_weighted_score += score * weights[criterion]
            total_weights += weights[criterion]
    
    if total_weights == 0:
        return 0.0
    
    return total_weighted_score / total_weights


def normalize_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Normalize a score to be within a specified range
    """
    if max_val == min_val:
        return min_val
    
    normalized = (score - min_val) / (max_val - min_val)
    return max(min(normalized, 1.0), 0.0)


def rank_candidates(candidates: List[Dict[str, Any]], sort_key: str = "overall_score") -> List[Dict[str, Any]]:
    """
    Rank candidates based on a specified metric
    """
    return sorted(candidates, key=lambda x: x.get(sort_key, 0), reverse=True)


def calculate_percentile(value: float, values_list: List[float]) -> float:
    """
    Calculate the percentile of a value compared to a list of values
    """
    if not values_list:
        return 0.0
    
    sorted_values = sorted(values_list)
    n = len(sorted_values)
    
    # Find the position of the value in the sorted list
    pos = 0
    for v in sorted_values:
        if value > v:
            pos += 1
        elif value == v:
            pos += 0.5  # Handle ties by taking middle position
    
    percentile = (pos / n) * 100
    return min(percentile, 100.0)


def apply_experience_penalty(years_of_experience: float, required_years: float) -> float:
    """
    Apply penalty for insufficient experience
    """
    if required_years == 0:
        return 1.0  # No penalty if no experience required
    
    if years_of_experience >= required_years:
        return 1.0  # Full score if experience meets or exceeds requirement
    else:
        # Apply penalty based on shortfall
        shortfall_ratio = (required_years - years_of_experience) / required_years
        penalty = min(shortfall_ratio * 0.5, 0.5)  # Max 50% penalty
        return max(1.0 - penalty, 0.0)


def calculate_skill_coverage(required_skills: List[str], available_skills: List[str]) -> float:
    """
    Calculate the percentage of required skills covered
    """
    if not required_skills:
        return 1.0  # If no skills required, full coverage
    
    required_set = set(skill.lower().strip() for skill in required_skills)
    available_set = set(skill.lower().strip() for skill in available_skills)
    
    matched_skills = required_set.intersection(available_set)
    coverage = len(matched_skills) / len(required_set)
    
    return coverage


def calculate_experience_relevance(past_roles: List[Dict[str, Any]], target_role: str) -> float:
    """
    Calculate how relevant past experience is to target role
    """
    if not past_roles:
        return 0.0
    
    relevant_count = 0
    target_lower = target_role.lower()
    
    for role in past_roles:
        role_title = role.get('role', '').lower()
        company = role.get('company', '').lower()
        
        # Check if role title or company is relevant
        if target_lower in role_title or target_lower in company:
            relevant_count += 1
    
    return relevant_count / len(past_roles)


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    Format a decimal value as a percentage string
    """
    percentage = value * 100
    return f"{round(percentage, decimal_places)}%"


def calculate_composite_score(components: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    Calculate composite scores from multiple components
    Each component has a score and weight
    """
    total_score = 0.0
    total_weight = 0.0
    
    for component_name, component_data in components.items():
        score = component_data.get('score', 0.0)
        weight = component_data.get('weight', 0.0)
        
        total_score += score * weight
        total_weight += weight
    
    if total_weight == 0:
        return {"composite_score": 0.0, "normalized_composite_score": 0.0}
    
    raw_composite = total_score / total_weight
    normalized_composite = normalize_score(raw_composite)
    
    return {
        "composite_score": raw_composite,
        "normalized_composite_score": normalized_composite
    }