export interface Summary {
  reportDate: string;
  overallAverages: {
    avgAnnualTuition: number;
    avgTotalDebt: number;
    avgEarningsYear2: number;
    avg5yrRoi: number;
    avgPaybackPeriodYears: number;
  };
  bestPerforming: {
    roiResult: {
      field: string;
      roi5yr: number;
      annualTuition: number;
      medianEarnings: number;
    };
    valueResult: {
      field: string;
      earningsPerDollar: number;
      annualTuition: number;
      medianEarnings: number;
    };
    paybackResult: {
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
  by5yrRoi: RankedField[];
  byEarningsPerDollar: RankedField[];
  byDebtToIncome: RankedField[];
  byPaybackPeriod: RankedField[];
}

interface FinancialMetrics {
  annualTuition: number;
  total4yrTuition: number;
  estimatedDebt: number;
  medianEarningsYear2: number;
}

interface RoiMetrics {
  earningsPerDollarTuition: number;
  earningsPerDollarComparison: string;
  roi5yrTuition: number;
  roiTuitionComparison: string;
  roi5YrDebt: number;
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
  cpi2018To2024: number;
  cpi2020To2024: number;
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
  roi5yr: number;
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
  roi5yr: number;
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
  earnings2018: number;
  earnings2024Adjusted: number;
  estimatedDebt: number;
  enrollment: number;
  totalTuition: number;
  debtToIncome: number;
  paybackYears: number;
  earnings5yr: number;
  roi5yrWithDebt: number;
  roi5yrWithTuition: number;
  earningsPerDollarTuition: number;
}

export interface FieldDataEntity extends TableRow {
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

export interface FieldData {
  id: number;
  field: string;
  tuition: number;
  earnings2018: number;
  earnings2024Adjusted: number;
  estimatedDebt: number;
  enrollment: number;
  totalTuition: number;
  debtToIncome: number;
  paybackYears: number;
  earnings5yr: number;
  roi5yrWithDebt: number;
  roi5yrWithTuition: number;
  earningsPerDollarTuition: number;
  createdAt: string;
}
