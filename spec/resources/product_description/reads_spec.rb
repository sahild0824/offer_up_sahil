require 'rails_helper'

RSpec.describe ProductDescriptionResource, type: :resource do
  describe 'serialization' do
    let!(:product_description) { create(:product_description) }

    it 'works' do
      render
      data = jsonapi_data[0]
      expect(data.id).to eq(product_description.id)
      expect(data.jsonapi_type).to eq('product_descriptions')
    end
  end

  describe 'filtering' do
    let!(:product_description1) { create(:product_description) }
    let!(:product_description2) { create(:product_description) }

    context 'by id' do
      before do
        params[:filter] = { id: { eq: product_description2.id } }
      end

      it 'works' do
        render
        expect(d.map(&:id)).to eq([product_description2.id])
      end
    end
  end

  describe 'sorting' do
    describe 'by id' do
      let!(:product_description1) { create(:product_description) }
      let!(:product_description2) { create(:product_description) }

      context 'when ascending' do
        before do
          params[:sort] = 'id'
        end

        it 'works' do
          render
          expect(d.map(&:id)).to eq([
            product_description1.id,
            product_description2.id
          ])
        end
      end

      context 'when descending' do
        before do
          params[:sort] = '-id'
        end

        it 'works' do
          render
          expect(d.map(&:id)).to eq([
            product_description2.id,
            product_description1.id
          ])
        end
      end
    end
  end

  describe 'sideloading' do
    # ... your tests ...
  end
end
