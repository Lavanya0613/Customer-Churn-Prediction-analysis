import pandas as pd
import numpy as np
import shap

class SHAPExplainer:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.preprocessor = pipeline.named_steps['preprocessor']
        self.classifier = pipeline.named_steps['classifier']
        self.feature_names = self.preprocessor.get_feature_names_out()
        
        # Note: LinearExplainer requires background data if standardizing, 
        # but since it's a linear model, the coefficients essentially define the explainer.
        # However, passing the model directly to LinearExplainer works well in modern SHAP.
        pass
        
    def _get_explainer(self, X_transformed_df):
        # We lazily instantiate the explainer using a sample to avoid passing full data at init
        return shap.LinearExplainer(self.classifier, X_transformed_df)

    def explain_instances(self, X_raw):
        """
        Takes raw features (dataframe), transforms them, and returns top positive and negative SHAP factors.
        """
        X_transformed = self.pipeline[:-1].transform(X_raw)
        X_transformed_df = pd.DataFrame(X_transformed, columns=self.feature_names)
        
        explainer = self._get_explainer(X_transformed_df)
        shap_values = explainer(X_transformed_df).values
        
        explanations = []
        for i in range(len(X_raw)):
            sv = shap_values[i]
            impacts = pd.DataFrame({'feature': self.feature_names, 'value': sv})
            
            # Sort factors
            increasing = impacts[impacts['value'] > 0].sort_values('value', ascending=False)
            decreasing = impacts[impacts['value'] < 0].sort_values('value', ascending=True)
            
            # Get just the top feature name for batch reporting
            top_risk = increasing.iloc[0]['feature'] if not increasing.empty else "None"
            top_protective = decreasing.iloc[0]['feature'] if not decreasing.empty else "None"
            
            # Get top 3 for detailed reporting
            top_3_risk = increasing.head(3)['feature'].tolist()
            top_3_protective = decreasing.head(3)['feature'].tolist()
            
            explanations.append({
                'top_risk_factor': top_risk,
                'top_protective_factor': top_protective,
                'top_3_risk_factors': top_3_risk,
                'top_3_protective_factors': top_3_protective
            })
            
        return explanations
