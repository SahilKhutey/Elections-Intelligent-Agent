"use client";

import React, { useEffect, useState } from 'react';
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';
import { MapPin, Navigation, Info, ExternalLink } from 'lucide-react';
import { useUser } from '../context/UserContext';
import { useLanguage } from '../context/LanguageContext';

const containerStyle = {
  width: '100%',
  height: '450px',
  borderRadius: '16px'
};

// Default center (Bhopal)
const defaultCenter = {
  lat: 23.2599,
  lng: 77.4126
};

export default function BoothMap() {
  const { user } = useUser();
  const { lang } = useLanguage();
  const [booths, setBooths] = useState<any[]>([]);
  const [center, setCenter] = useState(defaultCenter);
  const [selectedBooth, setSelectedBooth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

  useEffect(() => {
    // 1. Get user geolocation
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setCenter({
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
          });
        },
        () => console.warn("Geolocation permission denied. Using city default.")
      );
    }

    // 2. Fetch booths for the user's city
    fetch(`http://localhost:8000/api/booths?location=${user.location}`)
      .then(res => res.json())
      .then(data => {
        setBooths(data.booths || []);
        if (data.booths && data.booths.length > 0) {
          // Optionally center on the first booth if geolocation failed
          // setCenter({ lat: data.booths[0].lat, lng: data.booths[0].lng });
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch booths", err);
        setLoading(false);
      });
  }, [user.location]);

  const openInGoogleMaps = (lat: number, lng: number) => {
    window.open(`https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`, '_blank');
  };

  if (!API_KEY) {
    return (
      <div className="bg-white border border-[#E0E0E0] rounded-2xl p-8 text-center shadow-sm">
        <MapPin className="w-12 h-12 text-[#0B5FFF] mx-auto mb-4 opacity-20" />
        <h3 className="text-lg font-bold text-[#1A1A1A] mb-2">Map Integration Ready</h3>
        <p className="text-sm text-[#555555] max-w-sm mx-auto">
          Please add <code>NEXT_PUBLIC_GOOGLE_MAPS_API_KEY</code> to your environment variables to enable the polling booth locator.
        </p>
        <div className="mt-6 flex flex-col gap-3">
           {booths.map((b, i) => (
             <div key={i} className="text-left p-4 rounded-xl border border-[#E0E0E0] bg-[#F4F7FE]">
                <p className="font-bold text-[#1A1A1A]">{b.name}</p>
                <p className="text-xs text-[#555555]">{b.address}</p>
             </div>
           ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[#1A1A1A] flex items-center gap-2">
            <MapPin className="text-[#0B5FFF]" /> 
            {lang === 'hi' ? 'निकटतम मतदान केंद्र' : 'Nearby Polling Booths'}
          </h2>
          <p className="text-sm text-[#555555] mt-1 font-medium">
            {lang === 'hi' ? `${user.location} में आधिकारिक केंद्रों का पता लगाएं` : `Locate official voting centers in ${user.location}`}
          </p>
        </div>
        <div className="bg-[#F4F7FE] px-4 py-2 rounded-full text-[10px] font-bold text-[#0B5FFF] uppercase tracking-wider border border-[#0B5FFF]/10">
          Live Sync Active
        </div>
      </div>

      <div className="relative rounded-2xl overflow-hidden shadow-2xl shadow-[#0B5FFF]/5 border border-[#E0E0E0]">
        <LoadScript googleMapsApiKey={API_KEY}>
          <GoogleMap
            mapContainerStyle={containerStyle}
            center={center}
            zoom={14}
            options={{
              styles: mapStyles, // Minimalistic theme
              disableDefaultUI: false,
              zoomControl: true,
            }}
          >
            {/* User Location Marker */}
            <Marker 
              position={center} 
              icon="https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
              title="Your Location"
            />

            {/* Booth Markers */}
            {booths.map((booth, index) => (
              <Marker
                key={index}
                position={{ lat: booth.lat, lng: booth.lng }}
                onClick={() => setSelectedBooth(booth)}
                icon="https://maps.google.com/mapfiles/ms/icons/red-dot.png"
              />
            ))}

            {selectedBooth && (
              <InfoWindow
                position={{ lat: selectedBooth.lat, lng: selectedBooth.lng }}
                onCloseClick={() => setSelectedBooth(null)}
              >
                <div className="p-2 max-w-[200px]">
                  <h4 className="font-bold text-[#1A1A1A] mb-1">{selectedBooth.name}</h4>
                  <p className="text-xs text-[#555555] mb-3">{selectedBooth.address}</p>
                  <button 
                    onClick={() => openInGoogleMaps(selectedBooth.lat, selectedBooth.lng)}
                    className="w-full bg-[#0B5FFF] text-white py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1"
                  >
                    <Navigation className="w-3 h-3" /> Get Directions
                  </button>
                </div>
              </InfoWindow>
            )}
          </GoogleMap>
        </LoadScript>
      </div>

      {/* List View for accessibility */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {booths.map((booth, i) => (
          <div key={i} className="bg-white border border-[#E0E0E0] p-5 rounded-2xl hover:border-[#0B5FFF] transition-all group flex items-start justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-[#F4F7FE] flex items-center justify-center text-[#0B5FFF] group-hover:bg-[#0B5FFF] group-hover:text-white transition-all">
                <Info className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-[#1A1A1A]">{booth.name}</h4>
                <p className="text-xs text-[#555555] mt-1 font-medium">{booth.address}</p>
              </div>
            </div>
            <button 
              onClick={() => openInGoogleMaps(booth.lat, booth.lng)}
              className="p-2.5 rounded-lg bg-[#F4F7FE] text-[#0B5FFF] hover:bg-[#0B5FFF] hover:text-white transition-all shadow-sm"
              title="View in Google Maps"
            >
              <ExternalLink className="w-4 h-4" />
            </button>
          </div>
        ))}
        {booths.length === 0 && !loading && (
          <div className="col-span-full p-8 text-center bg-[#F4F7FE] rounded-2xl border border-dashed border-[#E0E0E0]">
            <p className="text-sm text-[#555555] font-medium italic">
              No polling booths indexed for {user.location} yet. Please check back later.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

// Minimalist Map Theme
const mapStyles = [
  {
    "featureType": "administrative",
    "elementType": "labels.text.fill",
    "stylers": [{ "color": "#444444" }]
  },
  {
    "featureType": "landscape",
    "elementType": "all",
    "stylers": [{ "color": "#f2f2f2" }]
  },
  {
    "featureType": "poi",
    "elementType": "all",
    "stylers": [{ "visibility": "off" }]
  },
  {
    "featureType": "road",
    "elementType": "all",
    "stylers": [{ "saturation": -100 }, { "lightness": 45 }]
  },
  {
    "featureType": "road.highway",
    "elementType": "all",
    "stylers": [{ "visibility": "simplified" }]
  },
  {
    "featureType": "road.arterial",
    "elementType": "labels.icon",
    "stylers": [{ "visibility": "off" }]
  },
  {
    "featureType": "transit",
    "elementType": "all",
    "stylers": [{ "visibility": "off" }]
  },
  {
    "featureType": "water",
    "elementType": "all",
    "stylers": [{ "color": "#0B5FFF" }, { "visibility": "on" }, { "lightness": 90 }]
  }
];
