require "rails_helper"

RSpec.describe "items_for_sales#create", type: :request do
  subject(:make_request) do
    jsonapi_post "/api/v1/items_for_sales", payload
  end

  describe "basic create" do
    let(:params) do
      {
        # ... your attrs here
      }
    end
    let(:payload) do
      {
        data: {
          type: "items_for_sales",
          attributes: params,
        },
      }
    end

    it "works" do
      expect(ItemsForSaleResource).to receive(:build).and_call_original
      expect do
        make_request
        expect(response.status).to eq(201), response.body
      end.to change { ItemsForSale.count }.by(1)
    end
  end
end
