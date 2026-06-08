import React, { useEffect, useState } from 'react';
import { Alert } from 'antd';

/**
 * Displays a banner when the application is offline. This component
 * listens for the browser's `online` and `offline` events and updates
 * its state accordingly. When offline, it renders an Ant Design
 * `Alert` with a warning message to inform the user that changes will
 * be synchronised once connectivity is restored.
 */
const OfflineIndicator: React.FC = () => {
  const [online, setOnline] = useState<boolean>(() => typeof navigator !== 'undefined' ? navigator.onLine : true);

  useEffect(() => {
    const handleOnline = () => setOnline(true);
    const handleOffline = () => setOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (online) return null;
  return (
    <Alert
      message="Offline mode"
      description="You are currently offline. Any changes you make will be queued and synchronised when connectivity returns."
      type="warning"
      showIcon
      banner
    />
  );
};

export default OfflineIndicator;