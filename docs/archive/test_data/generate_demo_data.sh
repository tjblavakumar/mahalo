#!/bin/bash
# Quick test data generation with LLM
# Usage: ./generate_demo_data.sh

echo "================================================"
echo "MAHALO Test Data Generation (LLM-Enhanced)"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/utils/generate_test_data_llm.py" ]; then
    echo "Error: Please run this script from MAHALO/mahalo-main directory"
    exit 1
fi

echo "Generating realistic demo data..."
echo ""
echo "This will create:"
echo "  - 10 JIRA stories with detailed descriptions"
echo "  - 5 JIRA bugs with reproduction steps"
echo "  - 2 sprints"
echo "  - 8 ServiceNow incidents"
echo "  - 6 deployments"
echo "  - 15 Splunk logs"
echo ""

python backend/utils/generate_test_data_llm.py --quick

echo ""
echo "================================================"
echo "Done! Your test data is ready."
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Start the backend services"
echo "  2. Check the data in the APIs"
echo "  3. Run check_services.py to verify"
echo ""
