require "rails_helper"

RSpec.describe "items_for_sales#index", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/items_for_sales", params: params
  end

  describe "basic fetch" do
    let!(:items_for_sale1) { create(:items_for_sale) }
    let!(:items_for_sale2) { create(:items_for_sale) }

    it "works" do
      expect(ItemsForSaleResource).to receive(:all).and_call_original
      make_request
      expect(response.status).to eq(200), response.body
      expect(d.map(&:jsonapi_type).uniq).to match_array(["items_for_sales"])
      expect(d.map(&:id)).to match_array([items_for_sale1.id,
                                          items_for_sale2.id])
    end
  end
end
