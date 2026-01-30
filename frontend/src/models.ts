export interface Summary {
  reportDate: string;
  overallAverages: {
    avgAnnualTuition: number;
    avgTotalDebt: number;
    avg_earnings_year_2: number;
    avg_5yr_roi: number;
    avgPaybackPeriodYears: number;
  };
  bestPerforming: {
    highestRoi: {
      field: string;
      roi_5yr: number;
      annualTuition: number;
      medianEarnings: number;
    };
    bestValue: {
      field: string;
      earningsPerDollar: number;
      annualTuition: number;
      medianEarnings: number;
    };
    fastestPayback: {
      field: string;
      paybackYears: number;
      debtToIncome: number;
    };
  };
}

export interface RankedField {
  rank: number;
  field: string;
  value: number;
}

export interface Rankings {
  by_5yr_roi: RankedField[];
  byEarningsPerDollar: RankedField[];
  byDebtToIncome: RankedField[];
  byPaybackPeriod: RankedField[];
}

interface FinancialMetrics {
  annualTuition: number;
  total_4yr_tuition: number;
  estimatedDebt: number;
  median_earnings_year_2: number;
}

interface RoiMetrics {
  earningsPerDollarTuition: number;
  earningsPerDollarComparison: string;
  roi_5yr_tuition: number;
  roiTuitionComparison: string;
  roi_5yr_debt: number;
}

interface DebtBurden {
  debtToIncomeRatio: number;
  paybackPeriodYears: number;
}

export interface FieldAnalysis {
  field: string;
  fieldDisplayName: string;
  financialMetrics: FinancialMetrics;
  roiMetrics: RoiMetrics;
  debtBurden: DebtBurden;
  enrollment: number;
}

export interface Analysis {
  fields: FieldAnalysis[];
}

interface InflationAdjustment {
  cpi_2018_to_2024: number;
  cpi_2020_to_2024: number;
}

interface DebtEstimation {
  method: string;
  formula: string;
  programLength: string;
}

interface RoiCalculation {
  earningsGrowth: number;
  basePeriod: string;
  tuitionRoiFormula: string;
  debtRoiFormula: string;
}

interface PaybackCalculation {
  incomeToDebtRepayment: number;
  taxRate: number;
  interestRate: number;
  formula: string;
}

interface EarningsPerDollar {
  formula: string;
}

interface Assumptions {
  inflationAdjustment: InflationAdjustment;
  debtEstimation: DebtEstimation;
  roiCalculation: RoiCalculation;
  paybackCalculation: PaybackCalculation;
  earningsPerDollar: EarningsPerDollar;
}

interface DataYears {
  tuition: string;
  earnings: string;
  enrollment: string;
  debt: string;
}

export interface Methodology {
  dataSources: string[];
  assumptions: Assumptions;
  limitations: string[];
  dataYears: DataYears;
}

interface HighEnrollmentLowRoi {
  field: string;
  enrollment: number;
  roi_5yr: number;
}

interface HighDebtBurden {
  field: string;
  debtToIncome: number;
  paybackYears: number;
}

interface AreasRequiringAttention {
  highEnrollmentLowRoi: HighEnrollmentLowRoi[];
  highDebtBurden: HighDebtBurden[];
}

interface BestPractice {
  field: string;
  roi_5yr: number;
  debtToIncome: number;
}

interface Recommendations {
  highEnrollmentLowRoiFields: string[];
  highDebtBurdenFields: string[];
  systemWide: string[];
}

export interface PolicyRecommendations {
  areasRequiringAttention: AreasRequiringAttention;
  bestPractices: BestPractice[];
  recommendations: Recommendations;
}

interface Visualization {
  name: string;
  filename: string;
  description: string;
}

export interface VisualizationsDetails {
  visualizations: Visualization[];
}

interface TableRow {
  field: string;
  tuition: number;
  earnings_2018: number;
  earnings_2024_adjusted: number;
  estimatedDebt: number;
  enrollment: number;
  totalTuition: number;
  debtToIncome: number;
  paybackYears: number;
  earnings5yr: number;
  roi_5yr_w_debt: number;
  roi_5yr_w_tuition: number;
  earningsPerDollarTuition: number;
}

export interface FieldData extends TableRow {
  id: number;
  createdAt: string;
}

export interface Table {
  roiTable: TableRow[];
}

export interface CompleteReport {
  summary: Summary;
  rankings: Rankings;
  analysis: Analysis;
  methodology: Methodology;
  policyRecommendations: PolicyRecommendations;
  visualizations: VisualizationsDetails;
  table: Table;
}
