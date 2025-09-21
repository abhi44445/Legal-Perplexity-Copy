import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ConstitutionChatPage from './pages/ConstitutionChatPage'
import RightsExplorerPage from './pages/RightsExplorerPage'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/constitution" element={<ConstitutionChatPage />} />
          <Route path="/know-your-rights" element={<RightsExplorerPage />} />
          {/* Add more routes as we build more pages */}
        </Routes>
      </div>
    </Router>
  )
}

export default App
