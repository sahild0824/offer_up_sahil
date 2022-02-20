require 'rails_helper'

RSpec.describe "product_descriptions#destroy", type: :request do
  subject(:make_request) do
    jsonapi_delete "/api/v1/product_descriptions/#{product_description.id}"
  end

  describe 'basic destroy' do
    let!(:product_description) { create(:product_description) }

    it 'updates the resource' do
      expect(ProductDescriptionResource).to receive(:find).and_call_original
      expect {
        make_request
        expect(response.status).to eq(200), response.body
      }.to change { ProductDescription.count }.by(-1)
      expect { product_description.reload }
        .to raise_error(ActiveRecord::RecordNotFound)
      expect(json).to eq('meta' => {})
    end
  end
end
