require "rails_helper"

RSpec.describe "items_for_sales#destroy", type: :request do
  subject(:make_request) do
    jsonapi_delete "/api/v1/items_for_sales/#{items_for_sale.id}"
  end

  describe "basic destroy" do
    let!(:items_for_sale) { create(:items_for_sale) }

    it "updates the resource" do
      expect(ItemsForSaleResource).to receive(:find).and_call_original
      expect do
        make_request
        expect(response.status).to eq(200), response.body
      end.to change { ItemsForSale.count }.by(-1)
      expect { items_for_sale.reload }.
        to raise_error(ActiveRecord::RecordNotFound)
      expect(json).to eq("meta" => {})
    end
  end
end
