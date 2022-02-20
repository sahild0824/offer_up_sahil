require 'rails_helper'

RSpec.describe "items_for_sales#update", type: :request do
  subject(:make_request) do
    jsonapi_put "/api/v1/items_for_sales/#{items_for_sale.id}", payload
  end

  describe 'basic update' do
    let!(:items_for_sale) { create(:items_for_sale) }

    let(:payload) do
      {
        data: {
          id: items_for_sale.id.to_s,
          type: 'items_for_sales',
          attributes: {
            # ... your attrs here
          }
        }
      }
    end

    # Replace 'xit' with 'it' after adding attributes
    xit 'updates the resource' do
      expect(ItemsForSaleResource).to receive(:find).and_call_original
      expect {
        make_request
        expect(response.status).to eq(200), response.body
      }.to change { items_for_sale.reload.attributes }
    end
  end
end
