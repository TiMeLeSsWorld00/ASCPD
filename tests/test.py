import pytest

from src.html_parser import Html_paser
from html.parser import HTMLParser
import requests

def test_html_parser():
    assert Html_paser().parse_url('https://s-f.ca/') ==\
    {
        'text': "Creative Agency - Love Your Brand - Sajak & FarkiSajak & FarkiSajak & FarkiLove Your BrandWe are a creative agency building brands that people love.How We WorkFormGreat brands look the part. Design is the foundation of everything we do to help elevate your brand, maintain consistency and drive loyalty.Form ServicesArrow rightFunctionExceptional brand experiences are vital to fostering meaningful relationships. We build platforms that are intuitive, responsive and rewarding for both brand and consumer.Function ServicesArrow rightFlowKnowledge is power, as long as you use it. We monitor, analyze and optimize brand platforms to identify opportunity, refine media spend and ensure success.Flow ServicesArrow rightWorkGreat brands have great values. We show them off.VibationsBRANDING | PACKAGINGView case studyArrow rightdoppleWebsiteView case studyArrow rightRE/MAX HustleWebsite | Product DesignView case studyArrow rightNature's Heritage CannabisBRANDING | PACKAGINGView case studyArrow rightFalkbuiltWebsite | Lead FlowView case studyArrow rightSee all workArrow rightLet us help you love your brand.Great brands have great values. We show them off.Book Our ServicesArrow rightBook A Brand SessionArrow rightSajak & FarkiWorkArrow rightVibationsdoppleRE/MAX HustleNature's Heritage CannabisFalkbuiltSuperfluxVerizon / HBOCalgary Downtown AssociationAdFarmLive Resin ProjectNorthern BrewerBRWBOXMill St. BreweryDavid PellettierAboutArrow rightContactArrow rightMolson Bank Building\n#300, 116 8 Avenue SW\nCalgary, AB T2P 1B3Arrow rightInstagram© Sajak & Farki. All Rights Reserved.Love Your Brand",
        'links': ['/', '#', '/about#form', '/about#function', '/about#flow', '/work/vibations', '/work/dopple',
                  '/work/remax-hustle', '/work/natures-heritage-cannabis', '/work/falkbuilt', '/work', '/contact',
                  '/contact', '/', '/work', '/work/vibations', '/work/dopple', '/work/remax-hustle',
                  '/work/natures-heritage-cannabis', '/work/falkbuilt', '/work/superflux',
                  '/work/verizon-hbo-100-westeros', '/work/calgary-downtown-association', '/work/adfarm',
                  '/work/live-resin-project', '/work/norther-brewer', '/work/brwbox-holiday-advent-calendar',
                  '/work/Mill-st-brewery', '/work/david-pellettier-real-estate', '/about', '/contact',
                  'https://www.google.com/maps/place/Sajak+%26+Farki/@51.0457237,-114.0639609,15z/data=!4m5!3m4!1s0x0:0x7885fd3ad74f11c0!8m2!3d51.0457237!4d-114.0639609',
                  'https://www.instagram.com/sajakfarki/']}

    assert Html_paser().parse_text(requests.get('https://s-f.ca/').text) == Html_paser().parse_url('https://s-f.ca/')


